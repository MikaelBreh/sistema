from django.db.models import Sum, Q, F

from cadastros.models import Products_another_info
from produtos_acabados.models import TransferenciaEstoqueSaidaProdutos, MistoComponent, MistoItem
from vendas.models import PedidoSeparacao


def calcular_estoque_atual(produto):
    # Somar entradas do produto no estoque (considerando somente registros validados)
    entradas = TransferenciaEstoqueSaidaProdutos.objects.filter(
        Q(produto=produto) | Q(produto__products_another_info__produto_pertence=produto),
        numero_transferencia__validado=True
    ).aggregate(
        total_entrada=Sum('quantidade_unitaria')
    )['total_entrada'] or 0

    # Calcular saídas devido a itens mistos
    mistos_componentes = MistoComponent.objects.filter(
        content_type__model='products', object_id=produto.id
    ).aggregate(total_misto=Sum(
        F('quantidade') * F('misto_item__quantidade_de_caixas')))['total_misto'] or 0

    # Calcular adições de produtos mistos
    misto_items = MistoItem.objects.filter(
        content_type__model='products', object_id=produto.id
    ).aggregate(total_misto=Sum('quantidade_unitaria'))['total_misto'] or 0

    # Calcular saídas de pedidos finalizados
    saidas_pedidos_finalizados = PedidoSeparacao.objects.filter(
        Q(item_pedido__content_type__model='products', item_pedido__object_id=produto.id) |
        Q(item_pedido__content_type__model='products_another_info', item_pedido__object_id__in=Products_another_info.objects.filter(produto_pertence=produto).values_list('id', flat=True)),
        pedido__finalizado=True
    ).aggregate(total_finalizado=Sum('quantidade'))['total_finalizado'] or 0

    # Calcular o estoque final
    estoque_atual = entradas + misto_items - mistos_componentes - saidas_pedidos_finalizados

    return estoque_atual
