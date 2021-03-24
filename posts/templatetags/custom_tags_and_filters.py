from django.template.defaultfilters import register
# from django import template

# from posts.models import Post, Section, SubTitle, Title, Text, Citation, Image


# register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.inclusion_tag("posts/manage/section/section.html", takes_context=False)
def render_section(section):

    print('section tag', section)

    section_type = section.content_object._meta.model_name
    section_object = section.content_object

    return {
        'section_object': section_object,
        'section_type': section_type
    }
