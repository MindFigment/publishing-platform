from django import forms

from tags.utils import format_tags_into_string, parse_tags


class TagWidgetMixin:
    def format_value(self, value):
        if value is not None and not isinstance(value, str):
            value = format_tags_into_string(value)
        return super().format_value(value)


class TagWidget(TagWidgetMixin, forms.TextInput):
    pass


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super().clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(
                'You need to provide tags seperated by comma.'
            )

    def has_changed(self, initial_value, data_value):
        if self.disabled:
            return False

        try:
            data_value = self.clean(data_value)
        except forms.ValidationError:
            pass

        if initial_value is None:
            initial_value = []

        initial_value = [tag.name for tag in initial_value]

        return initial_value != data_value
