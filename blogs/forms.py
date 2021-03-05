from django import forms

from .models import Blog


class NewBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'subtitle', 'about', 'image', 'is_active')
