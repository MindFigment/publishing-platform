from django.db import models
from django.db.models.expressions import F

##################################
### FollowRelationship manager ###
##################################


class ExtendedManager(models.Manager):
    def seen(self, blog_id):
        return self.get_queryset() \
            .filter(blog=blog_id, seen=True)
        # .exclude(blog__author=F('profile'))

    def notseen(self, blog_id):
        return self.get_queryset() \
            .filter(blog=blog_id, seen=False)
        # .exclude(blog__author=F('profile'))
