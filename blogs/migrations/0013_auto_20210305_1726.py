# Generated by Django 3.1.7 on 2021-03-05 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210305_1657'),
        ('blogs', '0012_auto_20210305_1657'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followrelationship',
            unique_together={('profile', 'blog')},
        ),
    ]