from django.contrib import admin
from .models import Products, Clientes, Fornecedores, Materiais_de_Trabalho, Vendedores, TabelaPreco, \
    TabelaPrecoProduto, Products_another_info, KitItem


class TabelaPrecoProdutoInline(admin.TabularInline):
    model = TabelaPrecoProduto
    extra = 1

class TabelaPrecoAdmin(admin.ModelAdmin):
    inlines = [TabelaPrecoProdutoInline]


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'product_code', 'product_bar_code']  # Exemplo: nome, cod, codigo barras

class ClientesAdmin(admin.ModelAdmin):
    search_fields = ['name', 'cnpj', 'cidade']


admin.site.register(Products, ProductsAdmin)
admin.site.register(Products_another_info)
admin.site.register(KitItem)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Fornecedores)
admin.site.register(Materiais_de_Trabalho)
admin.site.register(Vendedores)
admin.site.register(TabelaPreco, TabelaPrecoAdmin)


