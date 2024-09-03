from cadastros.models import Products_another_info
from vendas.models import Pedido, PedidoSeparacao

from collections import defaultdict
from django.db.models import Exists, OuterRef


def verificar_quantidade_faltante():
    # Dicionário para armazenar a soma das quantidades faltantes por produto
    quantidades_faltantes = defaultdict(int)

    # Filtrar pedidos com status maior ou igual a 4 e menor que 12
    pedidos = Pedido.objects.filter(status__gte=4, status__lt=12)

    # Iterar sobre os pedidos
    for pedido in pedidos:
        # Iterar sobre os itens do pedido
        for item in pedido.itens.all():
            produto = item.produto

            # Verificar se o produto está associado ao modelo Products ou Products_another_info
            if isinstance(produto, Products_another_info):
                produto_base = produto.produto_pertence
            else:
                produto_base = produto

            # Obter todas as separações do item
            separacoes = item.separacoes.all()

            # Calcular a quantidade total separada
            quantidade_separada = sum(separacao.quantidade for separacao in separacoes)
            quantidade_faltante = item.quantidade - quantidade_separada

            # Somar a quantidade faltante ao total do produto base
            if quantidade_faltante > 0:
                quantidades_faltantes[produto_base.name] += quantidade_faltante

    return dict(quantidades_faltantes)



# --------------------------------------------------------------------------------------------

def verificar_quantidade_faltante_com_separacao_iniciada():
    # Dicionário para armazenar a soma das quantidades faltantes por produto
    quantidades_faltantes = defaultdict(int)

    # Subquery para verificar se o pedido tem alguma separação
    separacoes_existem = PedidoSeparacao.objects.filter(pedido=OuterRef('pk'))

    # Filtrar pedidos com status maior ou igual a 4 e menor que 12 e com separação iniciada
    pedidos = Pedido.objects.filter(
        status__gte=4, status__lt=12
    ).filter(Exists(separacoes_existem))

    # Iterar sobre os pedidos
    for pedido in pedidos:
        # Iterar sobre os itens do pedido
        for item in pedido.itens.all():
            produto = item.produto

            # Verificar se o produto está associado ao modelo Products ou Products_another_info
            if isinstance(produto, Products_another_info):
                produto_base = produto.produto_pertence
            else:
                produto_base = produto

            # Obter todas as separações do item
            separacoes = item.separacoes.all()

            # Calcular a quantidade total separada
            quantidade_separada = sum(separacao.quantidade for separacao in separacoes)
            quantidade_faltante = item.quantidade - quantidade_separada

            # Somar a quantidade faltante ao total do produto base
            if quantidade_faltante > 0:
                quantidades_faltantes[produto_base.name] += quantidade_faltante

    return dict(quantidades_faltantes)

