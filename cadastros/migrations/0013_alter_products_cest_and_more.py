# Generated by Django 5.0.1 on 2024-07-29 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0012_products_another_info_produto_pertence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='cest',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='products_another_info',
            name='produto_pertence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.products'),
        ),
    ]