# Generated by Django 4.1.2 on 2022-10-30 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0010_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category_lv',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Request and unique', max_length=255, unique=True, verbose_name='Nosaukums'),
        ),
    ]