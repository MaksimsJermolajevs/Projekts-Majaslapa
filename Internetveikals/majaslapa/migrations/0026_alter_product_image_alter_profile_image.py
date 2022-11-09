# Generated by Django 4.1.2 on 2022-11-07 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0025_remove_profile_avatar_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='images/default.png', help_text='Augšupielādējiet produkta attēlu', upload_to='images-product/', verbose_name='Attēls'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]