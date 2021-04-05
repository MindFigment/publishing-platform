from django.db import models
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.urls import reverse

from account.models import Profile
from tags.models import Tag
from .managers import ExtendedManager


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

    tags = models.ManyToManyField(Tag, through='TaggedBlog')

    objects = models.Manager()
    active = IsActiveManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.title} ({self.author.user.get_username()})'

    def get_absolute_url(self):
        return reverse('blogs:blog_detail',
                       args=[self.slug])

    def get_seen_followers(self):
        profile_ids = FollowRelationship.objects \
            .seen(blog_id=self.id) \
            .values_list('profile', flat=True)
        followers = Profile.objects.filter(id__in=profile_ids, following=self.id).annotate(
            created=F('following__created'))
        return followers

    def get_notseen_followers(self):
        profile_ids = FollowRelationship.objects \
            .notseen(self.id) \
            .values_list('profile', flat=True)
        followers = Profile.objects.filter(id__in=profile_ids, following=self.id).annotate(
            created=F('following__created'))
        return followers

    def set_followers_as_seen(self, followers):
        followers_ids = followers.values_list('id', flat=True)
        update = list(FollowRelationship.objects.filter(
            blog=self.id, profile__in=followers_ids))
        print('update before', [u.seen for u in update])
        for rel in update:
            rel.seen = True
        print('update after', [u.seen for u in update])
        FollowRelationship.objects.bulk_update(update, ['seen'])


class TaggedBlog(models.Model):
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog} tagged by {self.tag.name}'

    class Meta:
        unique_together = ('blog', 'tag')


class FollowRelationship(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='rel_from_set',
                                on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,
                             related_name='rel_to_set',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    seen = models.BooleanField(default=False)

    objects = ExtendedManager()
    # seen = SeenManager()
    # notseen = NotSeenManager()

    class Meta:
        ordering = ('-created',)
        unique_together = ('profile', 'blog')

    def __str__(self):
        return f'{self.profile} follows {self.blog} blog'
