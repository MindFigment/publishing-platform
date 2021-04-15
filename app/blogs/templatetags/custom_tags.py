import os

from django.conf import settings
from django.db.models import Q
from django.template.defaultfilters import register

from posts.models import Citation, Image, Text, Title

TITLE_MODEL_NAME = Title._meta.model_name
TEXT_MODEL_NAME = Text._meta.model_name
CITATION_MODEL_NAME = Citation._meta.model_name
IMAGE_MODEL_NAME = Image._meta.model_name


@register.inclusion_tag("posts/cards/post-card-simple.html", takes_context=False)
def post_card(post):
    post_sections = post.sections.order_by("order")
    post_title = post_sections.get(content_type__model=TITLE_MODEL_NAME)
    main_image = post_sections.filter(content_type__model=IMAGE_MODEL_NAME).first()
    if not main_image:
        main_image = os.path.join(
            settings.MEDIA_URL, "posts", "default", "default-post-image.jpeg"
        )
        image = main_image
    else:
        image = main_image.content_object.file

    first_paragraph = post_sections.filter(
        Q(content_type__model=TEXT_MODEL_NAME)
        | Q(content_type__model=CITATION_MODEL_NAME)
    ).first()

    if not first_paragraph:
        body = ""
        type = TEXT_MODEL_NAME
    else:
        if first_paragraph.content_object._meta.model_name == TEXT_MODEL_NAME:
            type = TEXT_MODEL_NAME
        else:
            type = CITATION_MODEL_NAME
        if type == TEXT_MODEL_NAME:
            body = first_paragraph.content_object.text
        else:
            body = first_paragraph.content_object.citation

    return {
        "post": post,
        "image": image,
        "title": post_title.content_object.title,
        "first_paragraph": body,
        "type": type,
    }
