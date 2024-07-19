# Generated by Django 5.0.1 on 2024-07-15 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastros', '0008_alter_clientes_tabelapreco'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferenciaEstoqueSaidaInfo',
            fields=[
                ('numero_transferencia', models.AutoField(primary_key=True, serialize=False)),
                ('data_saida', models.DateField(auto_now_add=True)),
                ('motorista', models.CharField(max_length=40)),
                ('veiculo', models.CharField(max_length=40)),
                ('conferente', models.CharField(max_length=40)),
                ('quantidade_pallets', models.IntegerField()),
                ('observacoes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TransferenciaEstoqueSaidaProdutos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_unitaria', models.IntegerField()),
                ('quantidade_caixa', models.IntegerField()),
                ('lote', models.CharField(max_length=20)),
                ('data_fabricacao', models.DateField()),
                ('validade', models.DateField()),
                ('numero_transferencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos_acabados.transferenciaestoquesaidainfo')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.products')),
            ],
        ),
    ]
