# Generated by Django 5.0.1 on 2024-12-30 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0003_alter_estoque_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventariosEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.CharField(blank=True, max_length=8, null=True)),
                ('lote', models.CharField(blank=True, max_length=10, null=True)),
                ('quantidade', models.IntegerField()),
                ('data', models.DateField(auto_now_add=True)),
            ],
            options={
                'permissions': [('ver_inventario_estoque', 'Can see stock inventory')],
            },
        ),
    ]
