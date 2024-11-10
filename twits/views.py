from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import CustomUser
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Twit, Comment
from .forms import CommentForm


class DashboardView(LoginRequiredMixin, ListView):
    """
    Display all Twits in reverse chronological order.
    Requires user to be logged in.
    """

    model = Twit
    template_name = "twits/dashboard.html"
    context_object_name = "twits"
    ordering = ["-created_at"]


class TwitCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Twit.
    Automatically sets the author to the current user.
    """

    model = Twit
    template_name = "twits/twit_form.html"
    fields = ["body", "image_url"]
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        """Set the author to the current user before saving."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TwitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing Twit.
    Only allows the author to make updates.
    """

    model = Twit
    template_name = "twits/twit_form.html"
    fields = ["body", "image_url"]
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        """Verify the current user is the author."""
        twit = self.get_object()
        return self.request.user == twit.author


class TwitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing Twit.
    Only allows the author to delete.
    """

    model = Twit
    template_name = "twits/twit_confirm_delete.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        """Verify the current user is the author."""
        twit = self.get_object()
        return self.request.user == twit.author


class UserPublicProfileView(ListView):
    """
    Display all Twits for a specific user in reverse chronological order.
    """

    model = Twit
    template_name = "twits/public_profile.html"
    context_object_name = "twits"

    def get_queryset(self):
        """
        Filter twits to show only those by the requested user.
        """
        self.profile_user = get_object_or_404(CustomUser, id=self.kwargs["pk"])  # Use CustomUser instead of User
        return Twit.objects.filter(author=self.profile_user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        """
        Add profile_user to the template context.
        """
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user
        return context


@login_required
@require_POST
def like_twit(request, pk):
    """
    Toggle like status for a Twit.
    Returns JSON with updated like count and status.
    """
    twit = get_object_or_404(Twit, pk=pk)
    is_liked = twit.likes.filter(id=request.user.id).exists()

    if is_liked:
        twit.likes.remove(request.user)
        liked = False
    else:
        twit.likes.add(request.user)
        liked = True

    return JsonResponse({"likes_count": twit.likes.count(), "liked": liked})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new comment on a specific Twit.
    """

    model = Comment
    # fields = ['body']
    form_class = CommentForm
    template_name = "twits/comment_form.html"

    def get_context_data(self, **kwargs):
        """
        Add the parent Twit to the template context.
        """
        context = super().get_context_data(**kwargs)
        context["twit"] = get_object_or_404(Twit, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        """
        Set the comment's author and Twit before saving.
        """
        form.instance.author = self.request.user
        form.instance.twit = get_object_or_404(Twit, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        """
        Return to the Twit's page after successful comment.
        """
        return reverse_lazy("dashboard")
