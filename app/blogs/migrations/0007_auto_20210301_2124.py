# Generated by Django 3.1.7 on 2021-03-01 21:24

from django.db import migrations, models

import blogs.models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(
                blank=True, upload_to=blogs.models.get_blog_image_dir_path),
        ),
    ]
