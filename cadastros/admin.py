from django.contrib import admin
from .models import Products, Clientes, Fornecedores, Materiais_de_Trabalho, Vendedores, TabelaPreco, \
    TabelaPrecoProduto, Products_another_info


class TabelaPrecoProdutoInline(admin.TabularInline):
    model = TabelaPrecoProduto
    extra = 1

class TabelaPrecoAdmin(admin.ModelAdmin):
    inlines = [TabelaPrecoProdutoInline]

admin.site.register(Products)
admin.site.register(Products_another_info)
admin.site.register(Clientes)
admin.site.register(Fornecedores)
admin.site.register(Materiais_de_Trabalho)
admin.site.register(Vendedores)
admin.site.register(TabelaPreco, TabelaPrecoAdmin)


