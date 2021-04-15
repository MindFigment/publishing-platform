from django.db import models
from django.conf import settings
from django.db.models.expressions import F
from django.urls import reverse
from django.db.models import Count
from django.apps import apps

# from django.contrib.auth.models import User


# User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              default='users/default/default_avatar.jpeg')
    about = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.get_username()}'

    def get_absolute_url(self):
        return reverse('profile_detail',
                       args=[self.user.username])

    def get_followers_count(self):
        return self.blogs.aggregate(count=Count('followers'))['count']

    def get_new_followers_count(self):
        return apps.get_model('blogs', 'FollowRelationship').objects.filter(
            blog__author__user=self.user
        ).filter(seen=False).count()

    def get_old_and_new_followers(self):
        followers = apps.get_model('blogs', 'FollowRelationship').objects.filter(
            blog__author__user=self.user
        )

        new_followers = followers.filter(
            seen=False).annotate(old=F('seen'))
        old_followers = followers.filter(seen=True).annotate(
            old=F('seen'))

        return old_followers, new_followers

    def set_followers_as_old(self, followers):
        for follower in followers:
            follower.seen = True
        apps.get_model('blogs', 'FollowRelationship').objects.bulk_update(
            followers, ['seen'])
