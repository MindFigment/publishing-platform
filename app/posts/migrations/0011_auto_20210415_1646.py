# Generated by Django 3.1.7 on 2021-04-15 16:46

from django.db import migrations, models
import posts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20210414_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to=posts.utils.get_post_image_dir_path),
        ),
    ]