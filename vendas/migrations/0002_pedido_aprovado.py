# Generated by Django 5.0.1 on 2024-07-31 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='aprovado',
            field=models.BooleanField(default=False),
        ),
    ]
