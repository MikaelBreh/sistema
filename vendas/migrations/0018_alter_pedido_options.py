# Generated by Django 5.0.1 on 2025-01-07 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0017_saidapedido_observacoes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'permissions': [('alterar_status', 'can chance status'), ('criar_pedido_amostra', 'can create sample order')]},
        ),
    ]
