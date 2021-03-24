from django.template.defaultfilters import stringfilter
from django import template
from django.utils.html import escape

from common.utils import add_markdown_to_links


register = template.Library()


@register.filter
# @stringfilter
def html_links(value):
    print('value', value)
    return add_markdown_to_links(escape(value))
