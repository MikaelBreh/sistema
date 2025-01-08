from django.contrib import admin
from .models import Estoque, InventariosEstoque

from django.utils.html import format_html
from django.urls import reverse

class EstoqueAdmin(admin.ModelAdmin):
    list_display = ['cod_produto', 'lote', 'quantidade', 'fonte_link', 'data', 'status', 'inventario']
    search_fields = ['cod_produto', 'lote']
    list_filter = ['status', 'inventario']

    def fonte_link(self, obj):
        if obj.fonte:
            content_type = obj.content_type
            url = reverse(f'admin:{content_type.app_label}_{content_type.model}_change', args=[obj.object_id])
            return format_html('<a href="{}">Detalhes</a>', url)
        return 'N/A'
    fonte_link.short_description = 'Origem'





# Registre o modelo com a classe personalizada
admin.site.register(Estoque, EstoqueAdmin),
admin.site.register(InventariosEstoque)

