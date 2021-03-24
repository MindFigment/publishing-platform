from django.utils.safestring import mark_safe
from django.urls import reverse


def get_image_preview(obj, image_field_name='image', alt_field_name='title'):
    print(obj.__dict__)
    HTML_IMG_LINK_TEMPLATE = '''
        <a href="{src}">
            <img src="{src}" alt="{alt} width="150" height="150" />
        </a>
    '''.strip()
    # if object has already been saved and has a primary key, show image preview
    image = getattr(obj, image_field_name)
    alt = getattr(obj, alt_field_name)
    if image and alt:
        html_str = HTML_IMG_LINK_TEMPLATE.format(src=image.url,
                                                 alt=alt)
        return mark_safe(html_str)
    else:
        return f'No image to preview! Set it first. Image: {image}, alt: {alt}'


get_image_preview.short_description = 'Image preview'


def get_edit_link(obj):
    HTML_LINK_TEMPLATE = '''
        <a href="{url}">{text}</a>
    '''.strip()
    print(obj)
    if obj.pk:
        admin_url_template = 'admin:{}_{}_change'.format(obj._meta.app_label,
                                                         obj._meta.model_name)
        admin_url = reverse(admin_url_template, obj.pk)
        text = 'Edit this {} separately'.format(obj._meta.verbose_name)
        html_str = HTML_LINK_TEMPLATE.format(url=admin_url,
                                             text=text)
        return mark_safe(html_str)


get_edit_link.short_description = 'Edit link'
