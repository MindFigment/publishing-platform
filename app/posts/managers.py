from django.db import models

# from posts.models import TitledQuerySet


# class PostManager(models.Manager):
#     def get_queryset(self):
#         return TitledQuerySet(
#             model=self.model,
#             using=self._db,
#             hints=self._hints
#         )


# class PublishedManager(PostManager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status='published')
