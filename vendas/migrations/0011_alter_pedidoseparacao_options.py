# Generated by Django 5.0.1 on 2024-10-01 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0010_alter_pedido_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedidoseparacao',
            options={'permissions': [('listar_pedidos_separacao', 'can list separations')]},
        ),
    ]
