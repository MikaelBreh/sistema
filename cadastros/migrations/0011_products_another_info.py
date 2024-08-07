# Generated by Django 5.0.1 on 2024-07-23 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0010_alter_products_box_bar_code_alter_products_cest_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products_another_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('product_code', models.CharField(blank=True, max_length=10, null=True)),
                ('product_bar_code', models.CharField(blank=True, max_length=13, null=True)),
                ('box_bar_code', models.CharField(blank=True, max_length=14, null=True)),
                ('box_quantity', models.IntegerField(blank=True, null=True)),
                ('ncm', models.CharField(blank=True, max_length=14, null=True)),
                ('cest', models.CharField(max_length=14)),
            ],
        ),
    ]
