from django.template.defaultfilters import register
from django.db.models import Q

from posts.models import Post, Section, Title, Text, Citation, Image


TITLE_MODEL_NAME = Title._meta.model_name
TEXT_MODEL_NAME = Text._meta.model_name
CITATION_MODEL_NAME = Citation._meta.model_name
IMAGE_MODEL_NAME = Image._meta.model_name


@register.inclusion_tag("blogs/post_card.html", takes_context=False)
def post_card(post):

    post_sections = post.sections.order_by('order')
    post_title = post_sections.get(content_type__model=TITLE_MODEL_NAME)
    print('post title:', post_title.content_object.title)
    main_image = post_sections.filter(
        content_type__model=IMAGE_MODEL_NAME).first()
    first_paragraph = post_sections.filter(
        Q(content_type__model=TEXT_MODEL_NAME) | Q(content_type__model=CITATION_MODEL_NAME)).first()

    type = TEXT_MODEL_NAME if first_paragraph.content_type._meta.model_name == TEXT_MODEL_NAME else CITATION_MODEL_NAME
    if type == TEXT_MODEL_NAME:
        body = first_paragraph.content_object.text
    else:
        body = first_paragraph.content_object.text

    print('main image:', main_image)
    print('first_paragraph:', first_paragraph)
    print('published', post.publish)
    return {
        'post': post,
        'image': main_image.content_object.file,
        'title': post_title.content_object.title,
        'first_paragraph': body,
        'type': type
    }
