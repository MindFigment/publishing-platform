from django import forms

from posts.models import Post
from blogs.models import Blog


class SearchForm(forms.Form):

    SEARCH_POSTS = 'posts.Post'
    SEARCH_BLOGS = 'blogs.Blog'

    MODEL_CHOICES = (
        (SEARCH_POSTS, 'post'),
        (SEARCH_BLOGS, 'blog')
    )

    BY_CHOICES = (
        ('title', 'title'),
        ('tags__name', 'tags')
    )

    query = forms.CharField()
    search_models = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=MODEL_CHOICES,
        initial=(SEARCH_POSTS, SEARCH_BLOGS),
    )
    search_fields = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=BY_CHOICES,
        initial=('title', 'tags__name'),
    )
