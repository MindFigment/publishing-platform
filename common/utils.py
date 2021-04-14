from django.core.checks.messages import Error
from django.template.defaultfilters import slugify

import re


def unique_slugify(instance, values, queryset=None, slug_field_name='slug', slug_seperator='-', max_num=1000):
    slug_field = instance._meta.get_field(slug_field_name)
    max_len = slug_field.max_length
    slug = slugify(values)
    if max_len:
        slug = slug[:max_len]

    if queryset is None:
        queryset = instance.__class__._default_manager.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    original_slug = slug

    num = 1
    while len(queryset.filter(**{slug_field_name: slug})) != 0:
        slug = original_slug
        end = f'{slug_seperator}{num}'
        if len(slug) + len(end) > max_len:
            overflow = len(slug) + len(end) - max_len
            slug = slug[:-overflow]

        slug = ''.join([slug, end])

        num += 1
        if num > max_num:
            raise Error(f'Over {max_num} slugs with the same base!')

    return slug


def add_markdown_to_links(text=None):
    regex = r'''(
                # scheme:// (https://)
                (?:(?:http|https)://){1}
                # domain name (no port so not authority) (www.example.com)
                (?:www\.)?(?:[a-z]+\.)*(?:[a-z]+)
                # path (/path/to/myfile.html)
                (?:/[a-zA-Z0-9_-]*)*(?:\.html)?
                # query/parameters (?key1=value1&key2=value2)
                (?:\?[a-z0-9]=[a-z0-9](?:[&;][a-z0-9]=[a-z0-9])*)?
                # anchor (#SomewhereInTheDocument)
                (?:\#(?:[a-zA-Z0-9_-]*))?
                )
                '''

    return re.sub(regex, _add_a_tag, text, flags=re.VERBOSE)


def _add_a_tag(match_obj):
    HTML_LINK = '<a href="{0}">{0}</a>'
    url = match_obj.group(0)
    return HTML_LINK.format(url)
