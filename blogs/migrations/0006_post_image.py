# Generated by Django 3.1.7 on 2021-03-01 20:11

import blogs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20210301_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to=blogs.models.get_image_dir_path),
        ),
    ]
