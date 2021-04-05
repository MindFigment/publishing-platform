from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
# from django.db.models.fields import related

from tags.models import Tag


# class Newspaper(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     # tags = models.ManyToManyField(
#     #     Tag, through='TaggedNewspaper', related_name='newspapers')


# class Article(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     newspaper = models.ForeignKey(
#         Newspaper, related_name='articles', on_delete=models.CASCADE
# )
# tags = models.ManyToManyField(
#     Tag, through='TaggedArticle', related_name='articles')


# class TaggedNewspaper(models.Model):
#     tag = models.ForeignKey(Tag,
#                             on_delete=models.CASCADE)
#     newspaper = models.ForeignKey(Newspaper,
#                                   on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.newspaper.name} tagged by {self.tag.name}'

#     class Meta:
#         unique_together = ('newspaper', 'tag')


# class TaggedArticle(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     tag = models.ForeignKey(Tag,
#                             related_name='tagged_articles',
#                             on_delete=models.CASCADE)
#     # article = models.ForeignKey(Article,
#     #                             on_delete=models.CASCADE)

#     # def __str__(self):
#     #     return f'{self.article.name} tagged by {self.tag.name}'

#     class Meta:
#         unique_together = ('name', 'tag')
