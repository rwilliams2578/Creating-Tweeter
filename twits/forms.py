"""
Name: Revelle Williams
Class: CIS 218
Date: November 28, 2024
"""

from django import forms
from .models import Twit
from .models import Comment


class TwitForm(forms.ModelForm):
    """
    Form for creating and editing Twits.
    Adds Bootstrap styling to form fields.
    """

    class Meta:
        model = Twit
        fields = ["body", "image_url"]
        labels = {"body": "Body*", "image_url": "Image url"}


class CommentForm(forms.ModelForm):
    """
    Form for creating comments on Twits.
    """

    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": "Text*"}
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            )
        }
