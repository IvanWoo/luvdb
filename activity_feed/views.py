from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView

from write.forms import ActivityFeedSayForm

from .models import Activity, Block, Follow

User = get_user_model()


class ActivityFeedView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "activity_feed/activity_feed.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["say_form"] = ActivityFeedSayForm()
        context["feed_type"] = "public"
        context["no_citation_css"] = True
        return context

    def post(self, request, *args, **kwargs):
        form = ActivityFeedSayForm(request.POST)
        if form.is_valid():
            say = form.save(commit=False)
            say.user = request.user
            say.save()
        return redirect("activity_feed:activity_feed")

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all().values_list("followed", flat=True)
        return (
            super()
            .get_queryset()
            .filter(user__in=list(following_users) + [user.id])
            .order_by("-timestamp")
        )


class ActivityFeedDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = "activity_feed/activity_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("activity_feed:activity_feed")


@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    # check if the logged-in user is blocked by the user they're trying to follow
    if Block.objects.filter(blocker=user_to_follow, blocked=request.user).exists():
        messages.error(
            request, "You have been blocked by this user and cannot follow them."
        )
        return redirect("accounts:detail", username=user_to_follow.username)

    # check if the logged-in user has blocked the user they're trying to follow
    if Block.objects.filter(blocker=request.user, blocked=user_to_follow).exists():
        messages.error(request, "You have blocked this user. Unblock them to follow.")
        return redirect("accounts:detail", username=user_to_follow.username)

    Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect("accounts:detail", username=user_to_follow.username)


@login_required
def unfollow(request, user_id):
    # Get the user to be unfollowed
    user_to_unfollow = User.objects.get(id=user_id)

    # Get the follow relationship
    follow_relationship = Follow.objects.filter(
        follower=request.user, followed=user_to_unfollow
    )

    # If the follow relationship exists, delete it
    if follow_relationship.exists():
        # Get the follow relationship instance before deleting it
        follow_instance = follow_relationship.first()

        # Delete the follow relationship
        follow_relationship.delete()

        # Get the content type for the Follow model
        content_type = ContentType.objects.get_for_model(Follow)

        # Delete the corresponding activity
        Activity.objects.filter(
            user=request.user,
            activity_type="follow",
            content_type=content_type,
            object_id=follow_instance.id,
        ).delete()

    # Redirect to the unfollowed user's profile page
    return redirect("accounts:detail", username=user_to_unfollow.username)


@login_required
def block_view(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        Block.objects.create(blocker=request.user, blocked=user_to_block)

        # If the blocker is following the blocked user, remove that follow relationship
        Follow.objects.filter(follower=request.user, followed=user_to_block).delete()

        # If the blocked user is following the blocker, remove that follow relationship
        Follow.objects.filter(follower=user_to_block, followed=request.user).delete()

        # You might also want to remove any activities related to the blocked user.
        content_type = ContentType.objects.get_for_model(User)
        Activity.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=user_to_block.id,
        ).delete()

        return redirect("accounts:detail", username=user_to_block.username)


@login_required
def unblock_view(request, user_id):
    user_to_unblock = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        Block.objects.filter(blocker=request.user, blocked=user_to_unblock).delete()

        # Depending on your requirements, you may want to re-establish follow relationships here.

        return redirect("accounts:detail", username=user_to_unblock.username)
