from django.contrib import admin

from cadastros.models import Products, Products_another_info
from .models import Pedido, PedidoItem, PedidoSeparacao, FaltandoSeparacao


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoItemInline]


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(FaltandoSeparacao)




class PedidoSeparacaoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'lote', 'quantidade', 'produto_nome')
    list_filter = ('pedido__status',)  # Filtro por status

    search_help_text = "Pesquise pelo nome do produto"

    def produto_nome(self, obj):
        # Lógica para exibir o nome do produto corretamente
        content_type = obj.item_pedido.content_type
        produto = obj.item_pedido.produto

        if content_type.model == 'products':
            return produto.name
        elif content_type.model == 'products_another_info':
            return produto.name

        return 'N/A'

    produto_nome.short_description = 'Nome do Produto'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Buscando nos modelos Products e Products_another_info
            produtos_ids = Products.objects.filter(name__icontains=search_term).values_list('id', flat=True)
            produtos_another_info_ids = Products_another_info.objects.filter(name__icontains=search_term).values_list('id', flat=True)

            # Filtrar o queryset para buscar pelo produto
            queryset = queryset.filter(
                item_pedido__object_id__in=list(produtos_ids) + list(produtos_another_info_ids),
                item_pedido__content_type__model__in=['products', 'products_another_info']
            )

        return queryset, use_distinct

admin.site.register(PedidoSeparacao, PedidoSeparacaoAdmin)








