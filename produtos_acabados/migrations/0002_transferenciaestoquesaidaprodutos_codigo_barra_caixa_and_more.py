# Generated by Django 5.0.1 on 2024-07-17 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos_acabados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferenciaestoquesaidaprodutos',
            name='codigo_barra_caixa',
            field=models.CharField(default=12345, max_length=14),
        ),
        migrations.AddField(
            model_name='transferenciaestoquesaidaprodutos',
            name='codigo_barra_unidade',
            field=models.CharField(default=1234, max_length=13),
        ),
    ]
