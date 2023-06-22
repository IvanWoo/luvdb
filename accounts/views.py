from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from activity_feed.models import Activity, Follow
from read.models import Book, Person
from write.models import Pin, Post, Say

from .forms import CustomUserCreationForm
from .models import InvitationCode

TIME_RESTRICTION = 365  # time restriction for generating invitation codes
User = get_user_model()


@login_required
def redirect_to_profile(request):
    return redirect("accounts:detail", username=request.user.username)


class SignUpView(CreateView):
    """View for user signup."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        # set invitation code as used
        if self.object.code_used:  # Check if the user used a code
            self.object.code_used.is_used = True
            self.object.code_used.save()

        return super().form_valid(form)


class AccountDetailView(LoginRequiredMixin, DetailView):
    """Detail view for user accounts."""

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "accounts/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the user has already generated an invitation code within the time restriction
        start_date = datetime.now() - timedelta(days=TIME_RESTRICTION)
        code_recently_generated = self.request.user.codes_generated.filter(
            generated_at__gte=start_date
        ).first()

        # Check if the code is used
        if code_recently_generated and code_recently_generated.is_used:
            context["can_generate_code"] = False
        else:
            context["can_generate_code"] = True

        user_posts = self.object.post_set.all().order_by("-timestamp")
        user_pins = self.object.pin_set.all().order_by("-timestamp")
        user_says = self.object.say_set.all().order_by("-timestamp")
        context["posts"] = user_posts
        context["pins"] = user_pins
        context["says"] = user_says
        context["recent_activities"] = Activity.objects.filter(
            user=self.object
        ).order_by("-timestamp")[:3]
        context["recent_following"] = Follow.objects.filter(
            follower=self.object
        ).order_by("-timestamp")[:5]
        context["recent_followers"] = Follow.objects.filter(
            followed=self.object
        ).order_by("-timestamp")[:5]

        context["no_citation_css"] = True
        context["no_text_input"] = True

        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for user accounts."""

    model = User
    fields = [
        "display_name",  # Add display_name to the list of fields
        "username",
        "bio",
    ]
    template_name = "accounts/account_update.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user


class GenerateInvitationCodeView(View):
    def post(self, request):
        user = request.user
        # Check if there is an unused code generated by the user
        unused_code = user.codes_generated.filter(is_used=False).first()
        if unused_code:
            code = unused_code
        elif not user.codes_generated.filter(
            generated_at__gte=timezone.now() - timedelta(days=TIME_RESTRICTION)
        ).exists():
            # User has not generated a code this month, so generate a new one
            code = InvitationCode.objects.create(generated_by=user)
        else:
            # User has already generated a code this month
            messages.error(
                request, "You can only generate one invitation code per month."
            )
            return redirect("accounts:profile")
        messages.success(
            request,
            mark_safe(
                f'Send this invitation code to your friend: <strong style="color:blue;">{code.code}</strong>.'
            ),
        )
        messages.success(request, "Every invitation code can only be used once. ")
        messages.success(request, "You can only invite one friend every month. ")
        return redirect("accounts:profile")


def home(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("activity_feed:activity_feed")
    else:
        return redirect("login")


def search_view(request):
    query = request.GET.get("q")
    if query:
        user_results = User.objects.filter(
            Q(username__icontains=query)
            | Q(display_name__icontains=query)
            | Q(bio__icontains=query)
        )
        post_results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        say_results = Say.objects.filter(content__icontains=query)
        pin_results = Pin.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(url__icontains=query)
        )
        person_results = Person.objects.filter(Q(name__icontains=query))
        book_results = Book.objects.filter(
            Q(book_title__icontains=query)
            | Q(isbn_10__icontains=query)
            | Q(isbn_13__icontains=query)
            | Q(asin__icontains=query)
            | Q(bookrole__person__name__icontains=query)
            | Q(bookrole__alt_name__icontains=query)
        )
    else:
        user_results = []
        post_results = []
        say_results = []
        pin_results = []
        person_results = []
        book_results = []

    return render(
        request,
        "accounts/search_results.html",
        {
            "query": query,
            "user_results": user_results,
            "post_results": post_results,
            "say_results": say_results,
            "pin_results": pin_results,
            "person_results": person_results,
            "book_results": book_results,
        },
    )


class PersonalActivityFeedView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "activity_feed/activity_feed.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_type"] = "personal"
        context["no_citation_css"] = True
        return context

    def get_queryset(self):
        # Get the username from the URL
        username = self.kwargs["username"]
        # Get the User object for this username
        user = User.objects.get(username=username)
        # Return only the activities for this user
        return super().get_queryset().filter(user=user).order_by("-timestamp")


class FollowingListView(ListView):
    model = Follow
    template_name = "accounts/following_list.html"
    context_object_name = "following_list"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs["username"])
        return user.following.all()


class FollowerListView(ListView):
    model = Follow
    template_name = "accounts/follower_list.html"
    context_object_name = "follower_list"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs["username"])
        return user.followers.all()
