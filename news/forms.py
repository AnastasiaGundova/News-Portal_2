from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category',
        ]

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get("title")
            text = cleaned_data.get("text")

            if title == text:
                raise ValidationError(
                    "The title cannot be identical to the content"
                )

            return cleaned_data
