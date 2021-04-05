from django import forms

from .models import Blog
from tags.forms import TagField, TagWidget
from tags.models import Tag


class NewBlogForm(forms.ModelForm):
    tags = TagField()

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.get('initial', {})
            initial['tags'] = kwargs['instance'].tags.all()
            kwargs['initial'] = initial
            print(kwargs)
            print(initial)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super().save(*args, commit=False, **kwargs)
        blog_tags = self.cleaned_data['tags']
        blog_tags = Tag.tags.add(*blog_tags)
        instance.tags.set(blog_tags)

        # If there is no commit argument it means we are commiting
        if kwargs.get('commit', True):
            instance.save()
            return instance

        return super().save(*args, **kwargs)

    class Meta:
        model = Blog
        fields = ('title', 'subtitle', 'about', 'image', 'is_active')
        # widgets = {
        #     'tags': TagWidget()
        # }
