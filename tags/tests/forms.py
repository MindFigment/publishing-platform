from django import forms

from blogs.models import Blog
from posts.models import Post


class MiniBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('tags',)


class MiniPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('tags',)
