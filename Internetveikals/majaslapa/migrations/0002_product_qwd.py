# Generated by Django 4.1.2 on 2023-01-05 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qwd',
            field=models.CharField(help_text='nepieciešams', max_length=255, null=True, verbose_name='Nosaukums'),
        ),
    ]
