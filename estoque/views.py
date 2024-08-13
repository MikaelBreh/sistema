from django.shortcuts import render
from django.db.models import Sum, F
from cadastros.models import Products
from produtos_acabados.models import TransferenciaEstoqueSaidaProdutos, MistoComponent, MistoItem
from vendas.models import PedidoSeparacao, PedidoItem
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def visualizar_estoque(request):
    produtos = Products.objects.all()
    search_query = request.GET.get('search', '')
    show_only_necessity = request.GET.get('necessidade', 'false') == 'true'
    order_by = request.GET.get('order_by', 'produto')

    if search_query:
        produtos = produtos.filter(name__icontains=search_query)

    estoque = []

    for produto in produtos:
        # Calcular entradas do produto no estoque
        entradas = TransferenciaEstoqueSaidaProdutos.objects.filter(produto=produto).aggregate(
            total_entrada=Sum('quantidade_unitaria'))['total_entrada'] or 0

        # Calcular saídas devido a itens mistos
        mistos_componentes = MistoComponent.objects.filter(
            content_type__model='products', object_id=produto.id
        ).aggregate(total_misto=Sum('quantidade'))['total_misto'] or 0

        # Calcular saídas devido a separação de pedidos
        separacao_pedidos = PedidoSeparacao.objects.filter(
            item_pedido__content_type__model='products', item_pedido__object_id=produto.id
        ).aggregate(total_separado=Sum('quantidade'))['total_separado'] or 0

        # Se for um produto misto, calcular a quantidade restante nos itens mistos
        if produto.category == 'misto':
            misto_items = MistoItem.objects.filter(
                content_type__model='products', object_id=produto.id
            ).aggregate(total_misto=Sum('quantidade_unitaria'))['total_misto'] or 0
            estoque_atual = misto_items - separacao_pedidos
        else:
            # Calcular o estoque final
            estoque_atual = entradas - mistos_componentes - separacao_pedidos

        # Calcular a necessidade de pedidos
        total_necessidade = PedidoItem.objects.filter(
            content_type__model='products', object_id=produto.id
        ).annotate(necessidade=F('quantidade') - Sum('separacoes__quantidade')).aggregate(
            total_necessidade=Sum('necessidade')
        )['total_necessidade'] or 0

        if show_only_necessity and total_necessidade <= 0:
            continue

        estoque.append({
            'produto': produto,
            'estoque_atual': estoque_atual,
            'necessidade_pedidos': total_necessidade
        })

    # Ordenação da lista de estoque
    if order_by.startswith('-'):
        reverse = True
        order_by = order_by[1:]
    else:
        reverse = False

    estoque = sorted(estoque, key=lambda x: getattr(x['produto'], 'name') if order_by == 'produto' else x[order_by],
                     reverse=reverse)

    # Paginação para 30 produtos por página
    paginator = Paginator(estoque, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'estoque/visualizar_estoque.html',
                  {'estoque': page_obj, 'search_query': search_query, 'show_only_necessity': show_only_necessity,
                   'order_by': order_by})

