from django.db import models
from django.db.models.aggregates import Count

from .utils import require_instance_manager


class ExtendedManager(models.Manager):
    def names(self):
        return self.get_queryset().values_list('name', flat=True)

    def slugs(self):
        return self.get_queryset().values_list('slug', flat=True)


class TaggableManager(models.Manager):
    def get_tags_with_no_tagged_items(self):
        return (
            self.get_queryset()
            .annotate(
                tagged_items=Count('taggedblog') + Count('taggedpost')
            )
            .filter(tagged_items=0)
        )

    def add(self, *tags):
        tag_objs = self._to_tag_model_instances(tags)
        return list(tag_objs)

    def remove(self, *tags):
        qs = self.get_queryset().filter(name__in=tags)
        qs.delete()

    # @require_instance_manager
    # def similar_items(self):

    def _to_tag_model_instances(self, tags):
        '''
        Takes an iterable containing either name strings, tags objects,
        or a mixture of both and returns set of tag objects
        '''
        str_tags = set()
        tag_objs = set()

        for t in tags:
            if isinstance(t, str):
                str_tags.add(t)
            elif isinstance(t, self.model):
                tag_objs.add(t)
            else:
                raise ValueError(
                    'Cannot add {} ({}). Expected {} or str'.format(
                        t, type(t), self.model
                    )
                )

        existing = self.filter(name__in=str_tags)
        tags_to_create = str_tags - set(t.name for t in existing)
        tag_objs.update(existing)

        for new_tag in tags_to_create:
            tag, _ = self.get_or_create(name=new_tag)
            tag_objs.add(tag)

        return tag_objs
