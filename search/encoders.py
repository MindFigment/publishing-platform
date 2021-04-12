import base64
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.db.models import Model

from posts.models import Post
from posts.models import Blog


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Blog):
            pass
        elif isinstance(o, Post):
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
        elif isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)
