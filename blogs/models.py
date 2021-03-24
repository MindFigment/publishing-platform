from django.db import models
from django.urls import reverse

from account.models import Profile


class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


def get_blog_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return 'blogs/{}-{}/images/{}'.format(instance.title,
                                          instance.author.user.username,
                                          filename)


def get_post_image_dir_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / ...
    return 'blogs/{}-{}-{}/images/posts/{}'.format(instance.blog.title,
                                                   instance.blog.author.first_name,
                                                   instance.blog.author.last_name,
                                                   filename)


class Blog(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    # author = models.ForeignKey(
    #     Profile, on_delete=models.CASCADE, related_name='blogs')
    is_active = models.BooleanField(default=True)
    about = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=get_blog_image_dir_path,
                              blank=True)

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='blogs')

    followers = models.ManyToManyField(Profile,
                                       through='FollowRelationship',
                                       related_name='following',
                                       symmetrical=False)

    objects = models.Manager()
    active = IsActiveManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.title} ({self.author.user.get_username()})'

    def get_absolute_url(self):
        return reverse('blogs:blog_detail',
                       args=[self.slug])


# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status='published')


# class Post(models.Model):
#     STATUS_CHOICES = (
#         ('draft', 'Draft'),
#         ('published', 'Published'),
#     )
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=255, unique_for_date='publish')
#     blog = models.ForeignKey(
#         Blog, on_delete=models.CASCADE, related_name='posts')
#     image = models.ImageField(upload_to=get_post_image_dir_path,
#                               blank=True)
#     body = models.TextField()
#     publish = models.DateTimeField(default=timezone.now)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     status = models.CharField(
#         max_length=10, choices=STATUS_CHOICES, default='draft')

#     objects = models.Manager()
#     published = PublishedManager()

#     class Meta:
#         ordering = ('-publish',)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('blogs:post_detail',
#                        args=[self.publish.year,
#                              self.publish.month,
#                              self.publish.day, self.slug])


class FollowRelationship(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='rel_from_set',
                                on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,
                             related_name='rel_to_set',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('profile', 'blog')

    def __str__(self):
        return f'{self.profile} follows {self.blog} blog'
