# Generated by Django 3.1.7 on 2021-03-04 21:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0007_auto_20210301_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='last_name',
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to='auth.user'),
            preserve_default=False,
        ),
    ]
