from django.contrib import admin

from .models import TransferenciaEstoqueSaidaInfo, TransferenciaEstoqueSaidaProdutos, MistoItem, MistoComponent


class TransferenciaInfoAdmin(admin.ModelAdmin):
    list_display = ['numero_transferencia', 'data_saida', 'motorista', 'quantidade_pallets']
    search_fields = ['numero_transferencia', 'data_saida', 'motorista']  # Exemplo: cod_produto, lote


class ProdutoInfoInfoAdmin(admin.ModelAdmin):
    list_display = ['numero_transferencia', 'produto', 'lote', 'quantidade_unitaria', 'codigo_barra_unidade']
    search_fields = ['numero_transferencia__numero_transferencia', 'produto__name', 'lote']
    list_filter = ['numero_transferencia__validado']  # Adiciona filtro para o campo validado


# Register your models here.
admin.site.register(TransferenciaEstoqueSaidaInfo, TransferenciaInfoAdmin)
admin.site.register(TransferenciaEstoqueSaidaProdutos, ProdutoInfoInfoAdmin)
admin.site.register(MistoItem)
admin.site.register(MistoComponent)
