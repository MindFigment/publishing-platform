import base64
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile

from posts.models import Post
from posts.models import Blog


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Blog):
            return _encode_blog(o)
        elif isinstance(o, Post):
            return _encode_post(o)
        elif isinstance(o, Model):
            return model_to_dict(o)
        elif isinstance(o, ImageFieldFile):
            return
        return super().default(o)


def _encode_post(o):
    blog_image = ''
    if o.blog.image:
        with open(o.blog.image.path, 'rb') as im:
            blog_image = base64.b64encode(im.read()).decode('utf-8')

    blog = {
        'id': o.blog.id,
        'title': o.blog.title,
        'url': o.blog.get_absolute_url(),
        'image': blog_image
    }

    author_image = ''
    if o.blog.author.photo:
        with open(o.blog.author.photo.path, 'rb') as im:
            author_image = base64.b64encode(im.read()).decode('utf-8')

    author = {
        'id': o.blog.author.id,
        'username': o.blog.author.user.username,
        'url': o.blog.author.get_absolute_url(),
        'image': author_image
    }

    post_image = ''
    if o.first_image:
        with open(o.first_image.path, 'rb') as im:
            post_image = base64.b64encode(im.read()).decode('utf-8')

    post = model_to_dict(o)
    post['publish'] = datetime.strftime(post['publish'], '%b %d, %Y')
    post['url'] = o.get_absolute_url()
    post['blog'] = blog
    post['author'] = author
    post['image'] = post_image
    post['title'] = o.title or ''
    post['text'] = o.first_text_section or ''

    return post


def _encode_blog(o):
    author_image = ''
    if o.author.photo:
        with open(o.author.photo.path, 'rb') as im:
            author_image = base64.b64encode(im.read()).decode('utf-8')

    author = {
        'id': o.author.id,
        'username': o.author.user.username,
        'url': o.author.get_absolute_url(),
        'image': author_image
    }

    created = datetime.strftime(o.created, '%b %d, %Y')
    blog = model_to_dict(o)

    blog_image = ''
    if o.image:
        with open(o.image.path, 'rb') as im:
            blog_image = base64.b64encode(im.read()).decode('utf-8')

    blog['author'] = author
    blog['url'] = o.get_absolute_url()
    blog['image'] = blog_image,
    blog['created'] = created

    return blog
