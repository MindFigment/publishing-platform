from django import forms
from django.forms import formset_factory

from tags.forms import TagField

from .models import Citation, Image, Post, SubTitle, Text


class PostForm(forms.ModelForm):
    tags = TagField(required=False)

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            initial = kwargs.get("initial", {})
            initial["tags"] = kwargs["instance"].tags.all()
            kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ("status",)


class TitleForm(forms.Form):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())
    title = forms.CharField(
        label="Title",
        widget=forms.Textarea(
            attrs={
                "class": "form-story-title",
                "placeholder": "Story title",
                "autocomplete": "off",
                "rows": 1,
            }
        ),
    )


class SubTitleForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = SubTitle
        fields = ("subtitle",)
        widgets = {
            "subtitle": forms.Textarea(
                attrs={
                    "class": "form-story-subtitle",
                    "placeholder": "Subtitle",
                    "autocomplete": "off",
                    "rows": 1,
                }
            )
        }


SubTitleFormset = formset_factory(SubTitleForm, extra=0)


class TextForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = Text
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-story-text",
                    "placeholder": "Text",
                    "autocomplete": "off",
                    "rows": 1,
                }
            )
        }

    def save(self, commit=True):
        return super(Text, self).save(commit=commit)


TextFormset = formset_factory(TextForm, extra=0)


class CitationForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = Citation
        fields = ("citation",)
        widgets = {
            "citation": forms.Textarea(
                attrs={
                    "class": "form-story-citation",
                    "placeholder": "Citation",
                    "autocomplete": "off",
                    "rows": 1,
                }
            )
        }


CitationFormset = formset_factory(CitationForm, extra=0)


class ImageForm(forms.ModelForm):
    order = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

    class Meta:
        model = Image
        fields = ("file",)
        required = ("file",)


ImageFormset = formset_factory(ImageForm, extra=0)
