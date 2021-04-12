from django import forms

from .models import Blog
from tags.forms import TagField
from tags.models import Tag


class NewBlogForm(forms.ModelForm):
    tags = TagField()

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.get('initial', {})
            initial['tags'] = kwargs['instance'].tags.all()
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, *args, author=None, commit=True, **kwargs):
        instance = super().save(*args, commit=False, **kwargs)
        if author is not None:
            instance.author = author

        if commit:
            instance.save()
            blog_tags = self.cleaned_data['tags']
            blog_tags = Tag.tags.add(*blog_tags)
            instance.tags.set(blog_tags)

        return instance

    class Meta:
        model = Blog
        fields = ('title', 'subtitle', 'about', 'image', 'is_active')
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'cleareable-file-input'
            })
        }
