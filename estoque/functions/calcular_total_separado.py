from django.db.models import Sum, Q

from cadastros.models import Products_another_info
from vendas.models import PedidoSeparacao


def calcular_total_separado(produto):
    # Calcular saídas devido a separação de pedidos não finalizados
    separacao_pedidos_nao_finalizados = PedidoSeparacao.objects.filter(
        Q(item_pedido__content_type__model='products', item_pedido__object_id=produto.id) |
        Q(item_pedido__content_type__model='products_another_info', item_pedido__object_id__in=Products_another_info.objects.filter(produto_pertence=produto).values_list('id', flat=True)),
        pedido__finalizado=False
    ).aggregate(total_separado=Sum('quantidade'))['total_separado'] or 0

    return separacao_pedidos_nao_finalizados
