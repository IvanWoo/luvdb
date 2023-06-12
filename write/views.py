from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from activity_feed.models import Activity

from .forms import CommentForm, PinForm, PostForm, SayForm
from .models import Comment, Pin, Post, Say

User = get_user_model()


class ShareDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_content_type = ContentType.objects.get_for_model(self.object)
        context["comments"] = Comment.objects.filter(
            content_type=post_content_type, object_id=self.object.id
        )
        context["comment_form"] = CommentForm()
        return context


class ShareDeleteView(DeleteView):
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        content_type = ContentType.objects.get_for_model(object)
        Activity.objects.filter(content_type=content_type, object_id=object.id).delete()
        return super().delete(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = "write/post_list.html"

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs["username"])
        return Post.objects.filter(author=self.user)


class PostDetailView(ShareDetailView):
    model = Post
    template_name = "write/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "write/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("write:post_detail", args=[str(self.object.id)])


class PostUpdateView(UpdateView):
    model = Post
    template_name = "write/post_update.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy("write:post_detail", kwargs={"pk": self.object.id})


class PostDeleteView(ShareDeleteView):
    model = Post
    template_name = "write/post_confirm_delete.html"
    success_url = reverse_lazy("activity_feed:activity_feed")


class SayListView(ListView):
    model = Say
    template_name = "write/say_list.html"

    def get_queryset(self):
        self.user = get_object_or_404(
            get_user_model(), username=self.kwargs["username"]
        )
        return Say.objects.filter(author=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.request.user
        return context


class SayDetailView(ShareDetailView):
    model = Say
    template_name = "write/say_detail.html"


class SayCreateView(LoginRequiredMixin, CreateView):
    model = Say
    form_class = SayForm
    # fields = ["content"]
    template_name = "write/say_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("write:say_detail", args=[str(self.object.id)])


class SayUpdateView(UpdateView):
    model = Say
    template_name = "write/say_update.html"
    form_class = SayForm

    def get_success_url(self):
        return reverse_lazy("write:say_detail", kwargs={"pk": self.object.id})


class SayDeleteView(ShareDeleteView):
    model = Say
    template_name = "write/say_confirm_delete.html"
    success_url = reverse_lazy("activity_feed:activity_feed")

    def delete(self, request, *args, **kwargs):
        say = self.get_object()
        content_type = ContentType.objects.get_for_model(say)
        Activity.objects.filter(
            user=request.user,
            activity_type="say",
            content_type=content_type,
            object_id=say.id,
        ).delete()

        return super().delete(request, *args, **kwargs)


class PinListView(ListView):
    model = Pin
    template_name = "write/pin_list.html"

    def get_queryset(self):
        self.user = get_object_or_404(
            get_user_model(), username=self.kwargs["username"]
        )
        return Pin.objects.filter(author=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.request.user
        return context


class PinDetailView(ShareDetailView):
    model = Pin
    template_name = "write/pin_detail.html"


class PinCreateView(LoginRequiredMixin, CreateView):
    model = Pin
    form_class = PinForm
    template_name = "write/pin_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("write:pin_detail", args=[str(self.object.id)])


class PinUpdateView(UpdateView):
    model = Pin
    template_name = "write/pin_update.html"
    form_class = PinForm

    def get_success_url(self):
        return reverse_lazy("write:pin_detail", kwargs={"pk": self.object.id})


class PinDeleteView(DeleteView):
    model = Pin
    template_name = "write/pin_confirm_delete.html"
    success_url = reverse_lazy("activity_feed:activity_feed")


def add_comment(request, app_label, model_name, object_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.content_type = ContentType.objects.get(
                app_label=app_label, model=model_name.lower()
            )
            comment.object_id = object_id
            comment.save()
            return redirect(comment.content_object.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, "write/add_comment.html", {"form": form})


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "write/comment_update.html"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "write/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()
