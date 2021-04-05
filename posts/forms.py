from posts.models import Text
from django import forms
from django.forms import formset_factory

from .models import Post, Title, SubTitle, Text, Image, Citation
from tags.forms import TagField


class PostForm(forms.ModelForm):
    tags = TagField()

    class Meta:
        model = Post
        fields = ('status',)


class TitleForm(forms.Form):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    title = forms.CharField(
        label='Title',
        widget=forms.Textarea(attrs={
            'class': 'form-story-title',
            'placeholder': 'Blog title',
            'autocomplete': 'off',
            'rows': 1
        })
    )


class SubTitleForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = SubTitle
        fields = ('subtitle',)
        widgets = {
            'subtitle': forms.Textarea(attrs={
                'class': 'form-story-subtitle',
                'placeholder': 'Subtitle',
                'autocomplete': 'off',
                'rows': 1
            })
        }


SubTitleFormset = formset_factory(SubTitleForm, extra=0)


# class TextForm(forms.Form):
#     text = forms.CharField(
#         label='Text',
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Text section'
#         })
#     )
#     order = OrderField(blank=True, for_fields=['post'])

class TextForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = Text
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-story-text',
                'placeholder': 'Text',
                'autocomplete': 'off',
                'rows': 1
                # 'cols': 1,
            })
        }

    def save(self, commit=True):
        print('order:', self.order)
        return super(Text, self).save(commit=commit)


TextFormset = formset_factory(TextForm, extra=0)


class CitationForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = Citation
        fields = ('citation',)
        widgets = {
            'citation': forms.Textarea(attrs={
                'class': 'form-story-citation',
                'placeholder': 'Citation',
                'autocomplete': 'off',
                'rows': 1
            })
        }


CitationFormset = formset_factory(CitationForm, extra=0)


class ImageForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    # file = forms.FileField()

    class Meta:
        model = Image
        fields = ('file',)
        required = ('file',)


ImageFormset = formset_factory(ImageForm, extra=0)


class DividerForm(forms.Form):
    pass
