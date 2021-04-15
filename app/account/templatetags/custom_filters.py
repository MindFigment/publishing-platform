from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils import timezone

from common.utils import add_markdown_to_links


register = template.Library()


@register.filter
def html_links(value):
    return mark_safe(add_markdown_to_links(escape(value)))


@register.filter
def time_passed(value):
    now = timezone.now()
    diff = now - value

    if diff.days >= 365:
        years = diff.days // 365
        return str(years) + (' year ago' if years == 1 else ' years ago')

    if diff.days >= 30:
        months = diff.days // 30
        return str(months) + (' month ago' if months == 1 else ' months ago')

    if diff.days >= 1:
        days = diff.days
        return str(days) + (' day ago' if days == 1 else ' days ago')

    hours = diff.seconds // (60 * 60)
    if hours >= 1:
        return str(hours) + (' hour ago' if hours == 1 else ' hours ago')

    minutes = diff.seconds // 60
    if minutes >= 1:
        return str(minutes) + (' minute ago' if minutes == 1 else ' minutes ago')

    return str(diff.seconds) + (' second ago' if diff.seconds == 1 else ' seconds ago')
