# Generated by Django 4.1.2 on 2022-11-04 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0018_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
