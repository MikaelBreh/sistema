# Generated by Django 5.0.1 on 2024-12-30 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_inventariosestoque_numero_inventario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventariosestoque',
            name='numero_inventario',
            field=models.IntegerField(),
        ),
    ]
