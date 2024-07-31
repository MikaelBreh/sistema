# Generated by Django 5.0.1 on 2024-07-07 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_remove_tabelapreco_produto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabelaprecoproduto',
            name='comissao_gerente_comercial',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='tabelaprecoproduto',
            name='comissao_vendedor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='tabelaprecoproduto',
            name='comissao_vendedor2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]