# Generated by Django 5.0.1 on 2025-01-05 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0012_estoque_inventario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoque',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]