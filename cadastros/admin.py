from django.contrib import admin
from .models import Products, Clientes, Fornecedores, Materiais_de_Trabalho, Vendedores

# Register your models here.
admin.site.register(Products)
admin.site.register(Clientes)
admin.site.register(Fornecedores)
admin.site.register(Materiais_de_Trabalho)
admin.site.register(Vendedores)
