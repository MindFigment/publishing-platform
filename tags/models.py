from django.db import models
from django.db.models.aggregates import Count
from django.db.models.signals import m2m_changed
from django.utils.text import slugify

from tags.managers import ExtendedManager, TaggableManager


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    objects = ExtendedManager()
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def tagged_items_changed(action, **kwargs):
    if action == 'post_remove':
        Tag.tags.get_tags_with_no_tagged_items().delete()


# Probably very bad idea to attach these signal handlers, very inefficient.
# Maybe Redis as cache could be a valid solution?
m2m_changed.connect(tagged_items_changed, sender='posts.TaggedPost')
m2m_changed.connect(tagged_items_changed, sender='blogs.TaggedBlog')


# class TaggedItem(models.Model):
#     tag = models.ForeignKey(Tag,
#                             related_name='rel_to_set',
#                             on_delete=models.CASCADE)


# class TaggedItem(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType,
#                                      on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return '{object} tagged with {name} ({slug})'.format(
#             object=self.content_object,
#             name=self.tag.name,
#             slug=self.tag.slug
#         )

#     class Meta:
#         index_together = ('content_type', 'object_id')
#         unique_together = ('content_type', 'object_id', 'tag')


# class TaggedItem(models.Model):
#     name = models.CharField(unique=True, max_length=100)
#     slug = models.SlugField(unique=True, max_length=100)

#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return '{object} tagged with {name} ({slug})'.format(
#             object=self.content_object,
#             name=self.name,
#             slug=self.slug
#         )

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         print('Saving tag', self.name, self.slug)
#         super().save(*args, **kwargs)
