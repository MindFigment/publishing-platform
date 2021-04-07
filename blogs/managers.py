from django.db import models
from django.db.models.expressions import F


class FollowRelationshipManager(models.Manager):
    def seen(self, blog_id):
        return self.get_queryset() \
            .filter(blog=blog_id, seen=True)

    def notseen(self, blog_id):
        return self.get_queryset() \
            .filter(blog=blog_id, seen=False)


class BlogIsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
