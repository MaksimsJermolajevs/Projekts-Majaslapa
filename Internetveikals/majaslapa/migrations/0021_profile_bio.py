# Generated by Django 4.1.2 on 2022-11-04 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0020_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, help_text='nav nepieciešams', verbose_name='Apraksts'),
        ),
    ]