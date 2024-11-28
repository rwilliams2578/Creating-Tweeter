"""
Name: Revelle Williams
Class: CIS 218
Date: November 28, 2024
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("twit/new/", views.TwitCreateView.as_view(), name="twit_create"),
    path("twit/<int:pk>/edit/", views.TwitUpdateView.as_view(), name="twit_update"),
    path("twit/<int:pk>/delete/", views.TwitDeleteView.as_view(), name="twit_delete"),
    path("user/<int:pk>/", views.UserPublicProfileView.as_view(), name="public_profile"),
    path("twit/<int:pk>/like/", views.like_twit, name="like_twit"),
    path("twit/<int:pk>/comment/new/", views.CommentCreateView.as_view(), name="comment_new"),
]
