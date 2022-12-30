# Generated by Django 4.1.2 on 2022-12-27 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0057_specification_name_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specification_name',
            name='product',
        ),
        migrations.AddField(
            model_name='specification',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Produkta_specifikacijaa', to='majaslapa.product'),
        ),
    ]