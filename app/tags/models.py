from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.text import slugify

from tags.managers import ExtendedManager, TaggableManager


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    objects = ExtendedManager()
    tags = TaggableManager()

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def tagged_items_changed(action, **kwargs):
    if action == "post_delete":
        Tag.tags.get_tags_with_no_tagged_items().delete()


# Probably very bad idea to attach these signal handlers, very inefficient.
# Maybe Redis as cache could be a valid solution?
m2m_changed.connect(tagged_items_changed, sender="posts.TaggedPost")
m2m_changed.connect(tagged_items_changed, sender="blogs.TaggedBlog")
