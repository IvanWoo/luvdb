import secrets

import auto_prefetch
import pytz
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from activity_feed.models import Activity, Follow


class InvitationCode(auto_prefetch.Model):
    """Model representing invitation codes."""

    code = models.CharField(max_length=100, unique=True, blank=True)
    is_used = models.BooleanField(default=False)
    generated_by = auto_prefetch.ForeignKey(
        "CustomUser",
        related_name="codes_generated",
        on_delete=models.CASCADE,
        null=True,
    )
    generated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a new code if one hasn't been assigned yet
            self.code = get_random_string(8)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class CustomUser(AbstractUser):
    """Custom user model."""

    code_used = auto_prefetch.OneToOneField(
        InvitationCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="used_by",
    )
    invited_by = auto_prefetch.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    display_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    pure_text_mode = models.BooleanField(default=False)
    timezone = models.CharField(
        max_length=50, choices=[(tz, tz) for tz in pytz.all_timezones], default="UTC"
    )
    custom_domain = models.CharField(max_length=100, blank=True, null=True)

    # fine-grained settings
    enable_replies_by_default = models.BooleanField(default=True)
    enable_share_to_feed_by_default = models.BooleanField(default=False)

    # deactivation
    is_deactivated = models.BooleanField(default=False)
    deactivated_at = models.DateTimeField(blank=True, null=True)

    RESERVED_USERNAMES = [
        "admin",
        "root",
        "system",
        "support",
        "about",
        "user",
        "read",
        "watch",
        "listen",
        "play",
        "write",
        "say",
        "pin",
        "post",
        "repost",
        "checkin",
        "release",
        "work",
        "instance",
        "game",
        "movie",
        "series",
        "episode",
        "issue",
        "book",
        "periodical",
    ]

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"username": self.username})

    def clean(self):
        # Call the base class clean method (important!)
        super(CustomUser, self).clean()

        # Check if username contains '@'
        if "@" in self.username:
            raise ValidationError("Username cannot contain '@' character.")

        # Check if the username is in reserved list
        if self.username in self.RESERVED_USERNAMES:
            raise ValidationError("This username is reserved and cannot be registered.")

    def save(self, *args, **kwargs):
        if self.username in self.RESERVED_USERNAMES:
            raise ValidationError("This username is reserved and cannot be registered.")

        # Check if the user has used an invitation code
        if self.code_used and self.is_active:
            # # Save the user instance before creating the Follow and Activity instances
            super().save(*args, **kwargs)

            if self.invited_by:
                # Get or create a Follow instance for the new user following the inviter
                follow_new_user, created = Follow.objects.get_or_create(
                    follower=self, followed=self.invited_by
                )

                # Get or create a Follow instance for the inviter following the new user
                follow_inviter, created = Follow.objects.get_or_create(
                    follower=self.invited_by, followed=self
                )
        else:
            super().save(*args, **kwargs)


@receiver(post_save, sender=Follow)
def create_follow_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.follower,
            activity_type="follow",
            content_object=instance,
        )


class InvitationRequest(auto_prefetch.Model):
    email = models.EmailField(unique=True)
    about_me = models.TextField(null=True, blank=True)
    is_invited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


@login_required
def get_followed_usernames(request):
    usernames = list(
        Follow.objects.filter(follower=request.user).values_list(
            "followed__username", flat=True
        )
    )
    return JsonResponse({"usernames": usernames})


class AppPassword(auto_prefetch.Model):
    user = auto_prefetch.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE, related_name="app_passwords"
    )
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(20)  # Generates a secure token
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.user.username}"


def encrypt_password(raw_password):
    cipher_suite = Fernet(settings.FERNET_KEY)
    return cipher_suite.encrypt(raw_password.encode()).decode()


def decrypt_password(encrypted_password):
    cipher_suite = Fernet(settings.FERNET_KEY)
    return cipher_suite.decrypt(encrypted_password.encode()).decode()


class BlueSkyAccount(auto_prefetch.Model):
    """Model for storing user's BlueSky account details."""

    user = auto_prefetch.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="bluesky_account"
    )
    bluesky_handle = models.CharField(max_length=100, unique=True)
    bluesky_pds_url = models.URLField(max_length=255)
    _bluesky_app_password = models.CharField(max_length=128)

    def set_bluesky_app_password(self, raw_password):
        self._bluesky_app_password = encrypt_password(raw_password)

    def get_bluesky_app_password(self):
        return decrypt_password(self._bluesky_app_password)

    def __str__(self):
        return self.bluesky_handle


class MastodonAccount(auto_prefetch.Model):
    user = auto_prefetch.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="mastodon_account"
    )
    mastodon_handle = models.CharField(max_length=100, unique=True)
    _mastodon_access_token = models.CharField(max_length=255)

    # Method to set the encrypted access token
    def set_mastodon_access_token(self, raw_token):
        self._mastodon_access_token = encrypt_password(
            raw_token
        )  # Assuming you have an encryption method

    # Method to get the decrypted access token
    def get_mastodon_access_token(self):
        return decrypt_password(
            self._mastodon_access_token
        )  # Assuming you have a decryption method

    def __str__(self):
        return self.mastodon_handle


class WebAuthnCredential(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    credential_id = models.TextField(unique=True)
    public_key = models.TextField()
    sign_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    aaguid = models.CharField(max_length=36, blank=True, null=True)
    key_name = models.CharField(
        max_length=255, blank=True, null=True
    )  # Optional field for key name

    def __str__(self):
        return f"Credential for {self.user}"


class BlacklistedDomain(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ip_address
