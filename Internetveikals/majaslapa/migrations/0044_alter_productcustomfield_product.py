# Generated by Django 4.1.2 on 2022-12-06 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('majaslapa', '0043_productcustomfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcustomfield',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Produkta_specifikacija', to='majaslapa.product'),
        ),
    ]
