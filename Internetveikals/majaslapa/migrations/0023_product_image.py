# Generated by Django 4.1.2 on 2022-11-05 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0022_remove_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='images/default.png', help_text='Augšupielādējiet produkta attēlu', upload_to='images/', verbose_name='Attēls'),
        ),
    ]
