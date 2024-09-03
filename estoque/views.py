from django.shortcuts import render
from cadastros.models import Products
from estoque.functions.calcular_estoque_atual import calcular_estoque_atual
from estoque.functions.calcular_necessidade_pedidos import verificar_quantidade_faltante, verificar_quantidade_faltante_com_separacao_iniciada
from estoque.functions.calcular_total_separado import calcular_total_separado
from vendas.models import PedidoItem
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F




@login_required
def visualizar_estoque(request):
    produtos = Products.objects.all()
    search_query = request.GET.get('search', '')
    show_only_necessity = request.GET.get('necessidade', 'false') == 'true'
    order_by = request.GET.get('order_by', 'produto')

    # Executar as funções para obter as quantidades faltantes
    quantidades_faltantes = verificar_quantidade_faltante()
    quantidades_faltantes_com_separacao_iniciada = verificar_quantidade_faltante_com_separacao_iniciada()

    if search_query:
        produtos = produtos.filter(name__icontains=search_query)

    estoque = []

    for produto in produtos:
        # Calcular o estoque atual e total separado
        estoque_atual = calcular_estoque_atual(produto)
        total_separado = calcular_total_separado(produto)

        # Obter quantidades faltantes e quantidades faltantes com separação iniciada
        quantidade_faltante = quantidades_faltantes.get(produto.name, 0)
        quantidade_faltante_separacao_iniciada = quantidades_faltantes_com_separacao_iniciada.get(produto.name, 0)

        # Calcular valores descontados
        quantidade_faltante = max(quantidade_faltante - estoque_atual, 0)
        quantidade_faltante_separacao_iniciada = max(quantidade_faltante_separacao_iniciada - estoque_atual, 0)

        if show_only_necessity and quantidade_faltante <= 0:
            continue

        estoque.append({
            'produto': produto,
            'estoque_atual': estoque_atual,
            'separado': total_separado,
            'necessidade_pedidos': quantidade_faltante,
            'quantidade_faltante': quantidade_faltante,
            'quantidade_faltante_separacao_iniciada': quantidade_faltante_separacao_iniciada,
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






