# Generated by Django 5.0.1 on 2024-07-03 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendedores',
            name='pix',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
