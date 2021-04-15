from django.db import models
from django.db.models.expressions import F
from django.urls import reverse

from account.models import Profile
from common.utils import unique_slugify
from tags.models import Tag

from .managers import BlogIsActiveManager, FollowRelationshipManager
from .utils import get_blog_image_dir_path


class Blog(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    about = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=get_blog_image_dir_path, blank=True)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blogs")

    followers = models.ManyToManyField(
        Profile,
        through="FollowRelationship",
        related_name="following",
        symmetrical=False,
    )

    tags = models.ManyToManyField(Tag, through="TaggedBlog")

    objects = models.Manager()
    active = BlogIsActiveManager()

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"{self.title} ({self.author.user.get_username()})"

    def get_absolute_url(self):
        return reverse("blogs:blog_detail", args=[self.slug])

    def get_new_followers(self):
        return FollowRelationship.objects.notseen(blog_id=self.id).annotate(
            old=F("seen")
        )

    def get_old_followers(self):
        return FollowRelationship.objects.seen(blog_id=self.id).annotate(old=F("seen"))

    def set_followers_as_old(self, followers):
        for follower in followers:
            follower.seen = True
        FollowRelationship.objects.bulk_update(followers, ["seen"])

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, [self.title])
        super().save(*args, **kwargs)


class TaggedBlog(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blog} tagged by {self.tag.name}"

    class Meta:
        unique_together = ("blog", "tag")


class FollowRelationship(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="rel_from_set", on_delete=models.CASCADE
    )
    blog = models.ForeignKey(Blog, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    seen = models.BooleanField(default=False)

    objects = FollowRelationshipManager()

    class Meta:
        ordering = ("-created",)
        unique_together = ("profile", "blog")

    def __str__(self):
        return f"{self.profile} follows {self.blog} blog"
