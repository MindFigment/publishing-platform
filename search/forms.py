from django import forms

from posts.models import Post
from blogs.models import Blog


class SearchForm(forms.Form):

    MODEL_CHOICES = (
        ('posts.Post', 'post'),
        ('posts.Post', 'blog')
    )

    BY_CHOICES = (
        ('title', 'title'),
        ('tags__name', 'tags')
    )

    query = forms.CharField()
    search_models = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=MODEL_CHOICES,
        initial=('posts.Post', 'posts.Post'),
    )
    search_fields = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=BY_CHOICES,
        initial=('title', 'tags__name'),
    )
