# Generated by Django 5.0.1 on 2024-12-31 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0009_inventariosestoque_nome_produtos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventariosestoque',
            name='nome_produtos',
            field=models.CharField(max_length=60),
        ),
    ]
