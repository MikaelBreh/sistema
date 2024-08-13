# Generated by Django 5.0.1 on 2024-08-09 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('vendas', '0003_pedidoseparacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoitem',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),
        ),
    ]