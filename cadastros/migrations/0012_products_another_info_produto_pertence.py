# Generated by Django 5.0.1 on 2024-07-23 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0011_products_another_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='products_another_info',
            name='produto_pertence',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cadastros.products'),
        ),
    ]
