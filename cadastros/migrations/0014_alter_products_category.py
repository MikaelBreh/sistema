# Generated by Django 5.0.1 on 2024-08-05 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0013_alter_products_cest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(choices=[('fabricado', 'Fabricado'), ('misto', 'Misto'), ('kit', 'Kit'), ('kit_variavel', 'Kit Variável'), ('materia_prima', 'Matéria Prima')], max_length=15),
        ),
    ]
