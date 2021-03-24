from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.template.loader import render_to_string

from blogs.models import Blog
from .fields import OrderField


def get_post_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return 'blogs/{slug}/images/posts/{filename}'.format(slug=instance.blog.slug,
                                                         filename=filename)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='posts')
    # image = models.ImageField(upload_to=get_post_image_dir_path,
    #                           blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'Post on {self.blog.title} blog'

    def get_absolute_url(self):
        return reverse('posts:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


class Section(models.Model):
    '''
    Section
    '''
    # POSTS_APP = 'posts'
    # Available section types
    SECTION_TYPES = \
        models.Q(app_label='posts', model='title') | \
        models.Q(app_label='posts', model='subtitle') | \
        models.Q(app_label='posts', model='text') | \
        models.Q(app_label='posts', model='citation') | \
        models.Q(app_label='posts', model='image')

    # Every section is related to specific post
    post = models.ForeignKey(Post,
                             related_name='sections',
                             related_query_name='section',
                             on_delete=models.CASCADE)
    # Generic Foreign Key
    # table_id
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to=SECTION_TYPES)
    # row id
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Keeping track of post sections order
    order = OrderField(blank=True, for_fields=['post'])

    class Meta:
        unique_together = ('content_type', 'object_id')
        ordering = ('order',)

    def __str__(self):
        return f'post: {self.post.slug}, order: {self.order}, content: {self.content_type}'


class ContentBase(models.Model):
    sections_relation = GenericRelation(Section,
                                        content_type_field='content_type',
                                        object_id_field='object_id',
                                        related_query_name='%(class)s')

    @property
    def section(self):
        # Return the object if exists else None
        return self.sections_relation.first()

    class Meta:
        abstract = True

    def __str__(self):
        return f'ContentBase'

    def render(self):
        return render_to_string(f'posts/content/{self._meta.model_name}.html',
                                {'item': self})


class Title(ContentBase):
    title = models.TextField(max_length=50)


class SubTitle(ContentBase):
    subtitle = models.TextField(max_length=100)


class Text(ContentBase):
    text = models.TextField()


class Citation(ContentBase):
    citation = models.TextField()


class Image(ContentBase):
    file = models.FileField(upload_to='images')


# class Video(ContentBase):
#     url = models.URLField()


# <hr width="50%" size="8" align="center">
