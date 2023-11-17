import json
import random
import re
import string
from urllib.parse import urlparse

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import models, transaction
from django.db.models import Q
from django.db.models.signals import m2m_changed, post_delete, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from activity_feed.models import Activity, Block
from discover.models import Vote
from notify.models import MutedNotification, Notification
from notify.views import create_mentions_notifications

from .utils_bluesky import create_bluesky_post
from .utils_mastodon import create_mastodon_post

User = get_user_model()


def handle_tags(instance, content):
    instance.tags.clear()
    tags = set(re.findall(r"#(\w+)", content))
    for tag in tags:
        tag_obj, created = Tag.objects.get_or_create(name=tag)
        instance.tags.add(tag_obj)


def find_mentioned_users(content):
    usernames = re.findall(r"@(\w+)", content)
    return User.objects.filter(username__in=usernames)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def model_name(self):
        return "Tag"


class Project(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False, blank=True)

    def __str__(self):
        return self.name

    def model_name(self):
        return "Project"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Polymorphic relationship to Post, Say, or Pin
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    anchor = models.CharField(max_length=4, blank=True, editable=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.content_object}"

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def model_name(self):
        return "Comment"

    def save(self, *args, **kwargs):
        if not self.anchor:
            self.anchor = self.generate_unique_anchor()

        is_new = self.pk is None
        super().save(*args, **kwargs)

        is_blocked = Block.objects.filter(
            blocker=self.content_object.user, blocked=self.user
        ).exists()

        if is_blocked:
            raise PermissionDenied("You are blocked by the user and cannot comment.")

        has_muted = MutedNotification.objects.filter(
            user=self.content_object.user,
            content_type=ContentType.objects.get_for_model(self.content_object),
            object_id=self.content_object.id,
        ).exists()

        if is_new and not has_muted and self.user != self.content_object.user:
            user_url = reverse("accounts:detail", args=[self.user.username])
            user_name = (
                self.user.display_name if self.user.display_name else self.user.username
            )
            content_url = self.content_object.get_absolute_url()
            content_name = self.content_object.__class__.__name__.capitalize()
            if "checkin" in content_name:
                content_name = f"{content_name[:-7]} Check-in"
            message = f'<a href="{user_url}">@{user_name}</a> commented on your <a href="{content_url}">{content_name}</a>.'

            notification = Notification.objects.create(
                recipient=self.content_object.user,
                sender_content_type=ContentType.objects.get_for_model(self.user),
                sender_object_id=self.user.id,
                subject_content_type=ContentType.objects.get_for_model(
                    self.content_object
                ),
                subject_object_id=self.content_object.id,
                notification_type="comment",
                message=message,
            )
            notification.save()
            content_url_with_read_marker = f"{content_url}?mark_read={notification.id}"
            # Update the message with the new URL containing the marker
            notification.message = f'<a href="{user_url}">@{user_name}</a> commented on your <a href="{content_url_with_read_marker}">{content_name}</a>.'
            notification.save()

        create_mentions_notifications(self.user, self.content, self)

    def generate_unique_anchor(self):
        existing_anchors = set(
            Comment.objects.filter(
                content_type=self.content_type, object_id=self.object_id
            ).values_list("anchor", flat=True)
        )

        while True:
            anchor = "".join(random.choices(string.ascii_letters + string.digits, k=4))
            if anchor not in existing_anchors:
                return anchor


class Repost(models.Model):
    original_activity = models.ForeignKey(
        Activity, on_delete=models.SET_NULL, related_name="reposts", null=True
    )
    original_repost = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name="reposts", null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    comments_enabled = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    votes = GenericRelation(Vote)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def get_absolute_url(self):
        return reverse("write:repost_detail", args=[str(self.id)])

    def get_activity_id(self):
        try:
            activity = Activity.objects.get(
                content_type__model="repost", object_id=self.id
            )
            return activity.id
        except ObjectDoesNotExist:
            return None

    def get_reposts(self):
        return Repost.objects.filter(original_repost=self).exclude(id=self.id)

    def get_votes(self):
        return self.votes.aggregate(models.Sum("value"))["value__sum"] or 0

    def model_name(self):
        return "Repost"

    def save(self, *args, **kwargs):
        is_blocked = Block.objects.filter(
            blocker=self.content_object.user, blocked=self.user
        ).exists()

        if is_blocked:
            raise PermissionDenied("You are blocked by the user and cannot comment.")

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            Activity.objects.create(
                user=self.user,
                activity_type="repost",
                content_object=self,
            )

            if self.content and hasattr(self.user, "bluesky_account"):
                try:
                    bluesky_account = self.user.bluesky_account
                    create_bluesky_post(
                        bluesky_account.bluesky_handle,
                        bluesky_account.bluesky_pds_url,
                        bluesky_account.get_bluesky_app_password(),  # Ensure this method securely retrieves the password
                        self.content,
                        self.id,
                        "Repost",
                    )
                except Exception as e:
                    print(f"Error creating Bluesky post: {e}")

            if self.content and hasattr(self.user, "mastodon_account"):
                try:
                    mastodon_account = self.user.mastodon_account
                    create_mastodon_post(
                        mastodon_account.mastodon_handle,
                        mastodon_account.get_mastodon_access_token(),  # Ensure this method securely retrieves the password
                        self.content,
                        self.id,
                        "Repost",
                    )
                except Exception as e:
                    print(f"Error creating Mastodon post: {e}")

            original_activity_user = (
                self.original_activity.user
                if self.original_activity
                else self.original_repost.user
            )

            # Check if user has muted notifications for the original activity
            has_muted = MutedNotification.objects.filter(
                user=original_activity_user,
                content_type=ContentType.objects.get_for_model(
                    self.original_activity.content_object
                    if self.original_activity
                    else self.original_repost.content_object
                ),
                object_id=(
                    self.original_activity.content_object.id
                    if self.original_activity
                    else self.original_repost.content_object.id
                ),
            ).exists()

            # Create notification for repost
            if not has_muted and self.user != original_activity_user:
                user_url = reverse("accounts:detail", args=[self.user.username])
                content_url = self.original_activity.content_object.get_absolute_url()
                content_name = (
                    self.original_activity.content_object.__class__.__name__.capitalize()
                )
                if "checkin" in content_name:
                    content_name = f"{content_name[:-7]} Check-in"

                repost_url = self.get_absolute_url()
                message = f'<a href="{user_url}">@{self.user.username}</a> reposted your <a href="{content_url}">{content_name}</a>. See the <a href="{repost_url}">Repost</a>.'

                notification = Notification.objects.create(
                    recipient=self.original_activity.user,
                    sender_content_type=ContentType.objects.get_for_model(self.user),
                    sender_object_id=self.user.id,
                    subject_content_type=ContentType.objects.get_for_model(
                        self.original_activity.content_object
                    ),
                    subject_object_id=self.original_activity.content_object.id,
                    notification_type="repost",
                    message=message,
                )
                notification.save()
                repost_url_with_read_marker = (
                    f"{repost_url}?mark_read={notification.id}"
                )
                # Update the message with the new URL containing the marker
                notification.message = f'<a href="{user_url}">@{self.user.username}</a> reposted your <a href="{content_url}">{content_name}</a>. See the <a href="{repost_url_with_read_marker}">Repost</a>.'
                notification.save()

        # Handle tags
        handle_tags(self, self.content)
        create_mentions_notifications(self.user, self.content, self)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    comments_enabled = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    projects = models.ManyToManyField(Project, blank=True)
    reposts = GenericRelation(Repost)
    votes = GenericRelation(Vote)

    def get_absolute_url(self):
        return reverse("write:post_detail", args=[str(self.id)])

    def get_activity_id(self):
        try:
            activity = Activity.objects.get(
                content_type__model="post", object_id=self.id
            )
            return activity.id
        except ObjectDoesNotExist:
            return None

    def get_votes(self):
        return self.votes.aggregate(models.Sum("value"))["value__sum"] or 0

    def model_name(self):
        return "Post"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Activity.objects.create(
                user=self.user,
                activity_type="post",
                content_object=self,
            )

            if hasattr(self.user, "bluesky_account"):
                try:
                    bluesky_account = self.user.bluesky_account
                    create_bluesky_post(
                        bluesky_account.bluesky_handle,
                        bluesky_account.bluesky_pds_url,
                        bluesky_account.get_bluesky_app_password(),  # Ensure this method securely retrieves the password
                        f'I posted "{self.title}" on LʌvDB\n\n' + self.content + "\n\n",
                        self.id,
                        "Post",
                    )
                except Exception as e:
                    print(f"Error creating Bluesky post: {e}")

            if hasattr(self.user, "mastodon_account"):
                try:
                    mastodon_account = self.user.mastodon_account
                    create_mastodon_post(
                        mastodon_account.mastodon_handle,
                        mastodon_account.get_mastodon_access_token(),  # Ensure this method securely retrieves the password
                        f'I posted "{self.title}" on LʌvDB\n\n' + self.content + "\n\n",
                        self.id,
                        "Post",
                    )
                except Exception as e:
                    print(f"Error creating Mastodon post: {e}")
        # Handle tags
        handle_tags(self, self.content)
        create_mentions_notifications(self.user, self.content, self)


class Say(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    comments_enabled = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reposts = GenericRelation(Repost)
    votes = GenericRelation(Vote)

    # private say / direct mention
    is_direct_mention = models.BooleanField(default=False)
    visible_to = models.ManyToManyField(User, related_name="visible_says", blank=True)

    def get_absolute_url(self):
        return reverse("write:say_detail", args=[str(self.id)])

    def get_activity_id(self):
        try:
            activity = Activity.objects.get(
                content_type__model="say", object_id=self.id
            )
            return activity.id
        except ObjectDoesNotExist:
            return None

    def get_votes(self):
        return self.votes.aggregate(models.Sum("value"))["value__sum"] or 0

    def model_name(self):
        return "Say"

    def save(self, *args, **kwargs):
        # Determine if the object is new (i.e., has no primary key)
        is_new = self.pk is None

        if self.content.startswith("@"):
            self.is_direct_mention = True
            mentioned_users = find_mentioned_users(self.content)

        # Call the parent class's save method to actually save the object
        super().save(*args, **kwargs)

        if self.is_direct_mention:
            self.visible_to.set(mentioned_users)
            self.visible_to.add(self.user)

        if is_new:
            Activity.objects.create(
                user=self.user,
                activity_type="say",
                content_object=self,
            )

            if hasattr(self.user, "bluesky_account"):
                try:
                    bluesky_account = self.user.bluesky_account
                    create_bluesky_post(
                        bluesky_account.bluesky_handle,
                        bluesky_account.bluesky_pds_url,
                        bluesky_account.get_bluesky_app_password(),  # Ensure this method securely retrieves the password
                        self.content,
                        self.id,
                        "Say",
                    )
                except Exception as e:
                    print(f"Error creating Bluesky post: {e}")

            if hasattr(self.user, "mastodon_account"):
                try:
                    mastodon_account = self.user.mastodon_account
                    create_mastodon_post(
                        mastodon_account.mastodon_handle,
                        mastodon_account.get_mastodon_access_token(),  # Ensure this method securely retrieves the password
                        self.content,
                        self.id,
                        "Say",
                    )
                except Exception as e:
                    print(f"Error creating Mastodon post: {e}")

        # Handle tags
        handle_tags(self, self.content)
        create_mentions_notifications(self.user, self.content, self)


class Pin(models.Model):
    title = models.TextField()
    url = models.URLField()
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    comments_enabled = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reposts = GenericRelation(Repost)
    votes = GenericRelation(Vote)

    def get_absolute_url(self):
        return reverse("write:pin_detail", args=[str(self.id)])

    def get_activity_id(self):
        try:
            activity = Activity.objects.get(
                content_type__model="pin", object_id=self.id
            )
            return activity.id
        except ObjectDoesNotExist:
            return None

    def get_votes(self):
        return self.votes.aggregate(models.Sum("value"))["value__sum"] or 0

    def model_name(self):
        return "Pin"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Activity.objects.create(
                user=self.user,
                activity_type="pin",
                content_object=self,
            )

            if hasattr(self.user, "bluesky_account"):
                try:
                    bluesky_account = self.user.bluesky_account
                    create_bluesky_post(
                        bluesky_account.bluesky_handle,
                        bluesky_account.bluesky_pds_url,
                        bluesky_account.get_bluesky_app_password(),  # Ensure this method securely retrieves the password
                        f'I pinned "{self.title}" ({urlparse(self.url).netloc}) on LʌvDB\n\n'
                        + self.content
                        + "\n\n",
                        self.id,
                        "Pin",
                    )
                except Exception as e:
                    print(f"Error creating Bluesky post: {e}")

            if hasattr(self.user, "mastodon_account"):
                try:
                    mastodon_account = self.user.mastodon_account
                    create_mastodon_post(
                        mastodon_account.mastodon_handle,
                        mastodon_account.get_mastodon_access_token(),  # Ensure this method securely retrieves the password
                        f'I pinned "{self.title}" ({urlparse(self.url).netloc}) on LʌvDB\n\n'
                        + self.content
                        + "\n\n",
                        self.id,
                        "Pin",
                    )
                except Exception as e:
                    print(f"Error creating Mastodon post: {e}")

        # Handle tags
        handle_tags(self, self.content)
        create_mentions_notifications(self.user, self.content, self)


# delete activity when a `write` is deleted
@receiver(post_delete, sender=Post)
@receiver(post_delete, sender=Say)
@receiver(post_delete, sender=Pin)
@receiver(post_delete, sender=Repost)
@receiver(post_delete, sender="read.ReadCheckIn")
@receiver(post_delete, sender="listen.ListenCheckIn")
@receiver(post_delete, sender="watch.WatchCheckIn")
@receiver(post_delete, sender="play.GameCheckIn")
@receiver(post_delete, sender="activity_feed.Follow")
def delete_activity(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    Activity.objects.filter(content_type=content_type, object_id=instance.id).delete()


# notify comment users when a `write` is deleted
@receiver(pre_delete, sender=Post)
@receiver(pre_delete, sender=Say)
@receiver(pre_delete, sender=Pin)
@receiver(pre_delete, sender=Repost)
@receiver(pre_delete, sender="read.ReadCheckIn")
@receiver(pre_delete, sender="listen.ListenCheckIn")
@receiver(pre_delete, sender="watch.WatchCheckIn")
@receiver(pre_delete, sender="play.GameCheckIn")
def notify_comment_users(sender, instance, **kwargs):
    # Get all the comments on the object being deleted
    comments = instance.comments.all()

    # For each comment, create a notification for the user
    for comment in comments:
        # Check if the user of the comment is the same as the user of the object
        if comment.user == instance.user:
            # If they are the same, return early and do not create a notification
            continue

        # Create a message for the notification
        message = f"A {sender.__name__} your commented was deleted, thus your comment was also deleted: <br><blockquote>{comment.content}</blockquote>"

        # Create the notification
        Notification.objects.create(
            recipient=comment.user,
            sender_content_type=ContentType.objects.get_for_model(instance.user),
            sender_object_id=instance.user.id,
            notification_type="comment_on_deleted",
            message=message,
        )


# notify comment user when comment is deleted by parent user
@receiver(pre_delete, sender=Comment)
def notify_comment_user_on_deletion(sender, instance, **kwargs):
    # Delay the execution of the following code until after the current transaction is committed
    def _notify_comment_user_on_deletion():
        # Check if the content_object of the comment is being deleted
        if (
            instance.content_object is not None
            and instance.content_object.pk is not None
        ):
            # If the content_object is not being deleted, check if the user of the comment is not the same as the user of the object
            if instance.user != instance.content_object.user:
                # Create a message for the notification
                content_url = instance.content_object.get_absolute_url()
                message = f"Your comment on a <a href={content_url}>{instance.content_object.__class__.__name__}</a> was deleted by the user: <br><blockquote>{instance.content}</blockquote>"

                # Create the notification
                Notification.objects.create(
                    recipient=instance.user,
                    sender_content_type=ContentType.objects.get_for_model(
                        instance.content_object.user
                    ),
                    sender_object_id=instance.content_object.user.id,
                    notification_type="comment_deleted_by_user",
                    message=message,
                )

    transaction.on_commit(_notify_comment_user_on_deletion)


@receiver(m2m_changed, sender=Post.projects.through)
def update_projects(sender, instance, action, **kwargs):
    if action == "post_remove" or action == "post_clear":
        # Only check projects if some are removed
        unused_projects = Project.objects.annotate(
            num_posts=models.Count("post")
        ).filter(num_posts=0)
        unused_projects.delete()


# delete repost when activity is deleted
@receiver(post_delete, sender=Activity)
def delete_repost(sender, instance, **kwargs):
    # Check if the associated object is a Repost
    if isinstance(instance.content_object, Repost):
        # Delete the Repost object
        instance.content_object.delete()


# delete say when activity is deleted
@receiver(post_delete, sender=Activity)
def delete_say(sender, instance, **kwargs):
    # Check if the associated object is a Repost
    if isinstance(instance.content_object, Say):
        # Delete the Repost object
        instance.content_object.delete()


class LuvList(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    source = models.URLField(blank=True, null=True)
    wikipedia = models.URLField(blank=True, null=True)

    user = models.ForeignKey(
        User,
        related_name="luvlists_created",
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(Vote)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("write:luvlist_detail", args=[str(self.id)])

    def get_votes(self):
        return self.votes.aggregate(models.Sum("value"))["value__sum"] or 0

    def model_name(self):
        return "LuvList"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        handle_tags(self, self.notes)


class ContentInList(models.Model):
    luv_list = models.ForeignKey(
        LuvList, related_name="contents", on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.luv_list.title}: {self.content_object}"


class Randomizer(models.Model):
    luv_list = models.ForeignKey(
        LuvList, related_name="randomizers", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    last_generated_item = models.ForeignKey(
        ContentInList,
        related_name="randomized_in",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    last_generated_datetime = models.DateTimeField(null=True, blank=True)
    randomized_order = models.TextField(null=True, blank=True)
    interval_in_seconds = models.IntegerField(default=86400)

    @classmethod
    def get_randomizer(cls, luv_list, user=None):
        return cls.objects.get_or_create(luv_list=luv_list, user=user)[0]

    def generate_item(self):
        now = timezone.now()

        # Determine the timezone to use
        if self.user:
            user_tz = pytz.timezone(
                self.user.timezone
            )  # Assuming you have a timezone field on your User model
        else:
            user_tz = pytz.UTC  # Universal timezone for public randomizer

        today = timezone.localtime(now, user_tz).date()
        last_generated_date = None

        if self.last_generated_datetime:
            last_generated_date = timezone.localtime(
                self.last_generated_datetime, user_tz
            ).date()

        if last_generated_date == today:
            return self.last_generated_item

        current_items = list(self.luv_list.contents.all())
        current_item_ids = {item.id for item in current_items}

        if not self.randomized_order:
            random_order = [
                item.id for item in random.sample(current_items, len(current_items))
            ]
        else:
            random_order = json.loads(self.randomized_order)
            random_order = [
                item_id for item_id in random_order if item_id in current_item_ids
            ]
            new_item_ids = current_item_ids - set(random_order)
            random_order.extend(random.sample(list(new_item_ids), len(new_item_ids)))

        if not random_order:
            random_order = [
                item.id for item in random.sample(current_items, len(current_items))
            ]

        next_item_id = random_order.pop(0)
        next_item = ContentInList.objects.get(id=next_item_id)

        self.last_generated_item = next_item
        self.last_generated_datetime = now
        self.randomized_order = json.dumps(random_order if random_order else None)

        self.save()
        return next_item
