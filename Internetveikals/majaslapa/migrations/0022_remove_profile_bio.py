# Generated by Django 4.1.2 on 2022-11-04 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0021_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]
