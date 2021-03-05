from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count


User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.get_username()}'

    def get_absolute_url(self):
        return reverse('profile_detail',
                       args=[self.user.username])

    def get_followers_count(self):
        return self.blogs.aggregate(count=Count('followers'))['count']
