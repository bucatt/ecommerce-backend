# Generated by Django 4.1.5 on 2023-01-11 16:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitebackend', '0003_alter_shoppingcartproduct_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
