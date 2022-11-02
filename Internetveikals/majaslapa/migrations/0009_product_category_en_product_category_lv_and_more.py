# Generated by Django 4.1.2 on 2022-10-07 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0008_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_en',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='majaslapa.category', verbose_name='Kategorija'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_lv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='majaslapa.category', verbose_name='Kategorija'),
        ),
        migrations.AddField(
            model_name='product',
            name='desciption_en',
            field=models.TextField(blank=True, help_text='nav nepieciešams', null=True, verbose_name='Apraksts'),
        ),
        migrations.AddField(
            model_name='product',
            name='desciption_lv',
            field=models.TextField(blank=True, help_text='nav nepieciešams', null=True, verbose_name='Apraksts'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(help_text='nepieciešams', max_length=255, null=True, verbose_name='Nosaukums'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_lv',
            field=models.CharField(help_text='nepieciešams', max_length=255, null=True, verbose_name='Nosaukums'),
        ),
    ]