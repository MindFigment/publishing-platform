from django.core.checks.messages import Error
from django.db.models import query
from django.template.defaultfilters import slugify


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

    setattr(instance, slug_field_name, slug)

    return slug
