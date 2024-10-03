from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from produtos_acabados.models import MistoItem, TransferenciaEstoqueSaidaInfo
from vendas.models import FaltandoSeparacao, PedidoItem, Pedido
from .models import Estoque
from cadastros.models import Products


@login_required
@permission_required('estoque.view_estoque', raise_exception=True)
def visualizar_estoque(request):
    # Filtro de busca por nome do produto
    search_query = request.GET.get('search', '')
    show_only_necessity = request.GET.get('necessidade', False)
    order_by = request.GET.get('order_by', 'nome')  # Valor padrão: 'nome'
    direction = request.GET.get('direction', 'asc')  # Direção padrão: 'asc' (crescente)

    # Definir a ordem de classificação com base na direção
    if direction == 'desc':
        order_by = f'-{order_by}'

    # Filtrar produtos por nome
    produtos = Products.objects.all()
    if search_query:
        produtos = produtos.filter(name__icontains=search_query)

    # Filtra estoques para os produtos encontrados
    estoques = Estoque.objects.filter(cod_produto__in=produtos.values('product_code'))

    # Agrupamento e soma do estoque por produto
    produtos_quantidades = estoques.values('cod_produto').annotate(
        estoque_total=Sum('quantidade')
    )

    # Filtrar itens de pedido relacionados aos produtos
    product_content_type = ContentType.objects.get_for_model(Products)
    pedido_itens = PedidoItem.objects.filter(
        content_type=product_content_type,
        object_id__in=produtos.values('id'),
        pedido__status__in=['aprovados', 'separando', 'separacao_finalizada']
    ).values('object_id').annotate(pedidos_total=Sum('quantidade'))

    # Dicionário de pedidos por produto
    pedidos_por_produto = {
        item['object_id']: item['pedidos_total']
        for item in pedido_itens
    }

    # Agora buscamos o nome, estoque mínimo, e aplicamos o filtro de necessidade
    produtos_detalhes = []
    for produto in produtos_quantidades:
        try:
            produto_detalhe = Products.objects.get(product_code=produto['cod_produto'])
            pedidos = pedidos_por_produto.get(produto_detalhe.id, 0)
            estoque_apos_pedidos = produto['estoque_total'] - pedidos

            # Verifica se o estoque é menor que o estoque mínimo (se a opção de necessidade for marcada)
            if not show_only_necessity or (produto['estoque_total'] < produto_detalhe.estoq_minimo):
                produtos_detalhes.append({
                    'nome': produto_detalhe.name,
                    'estoque_minimo': produto_detalhe.estoq_minimo,
                    'estoque_total': produto['estoque_total'],
                    'pedidos': pedidos,
                    'estoque_apos_pedidos': estoque_apos_pedidos,
                })
        except Products.DoesNotExist:
            pass

    # Ordenação dos produtos de acordo com o parâmetro escolhido
    produtos_detalhes = sorted(produtos_detalhes, key=lambda x: x[order_by.lstrip('-')], reverse=(direction == 'desc'))

    # Paginação
    page = request.GET.get('page', 1)
    paginator = Paginator(produtos_detalhes, 10)
    estoque_page = paginator.get_page(page)

    context = {
        'produtos_quantidades': estoque_page,
        'search_query': search_query,
        'show_only_necessity': show_only_necessity,
        'estoque': estoque_page,
        'order_by': order_by.lstrip('-'),  # Passa o campo de ordenação atual
        'direction': direction,  # Passa a direção atual
    }

    return render(request, 'estoque/visualizar_estoque.html', context)


@login_required
@permission_required('estoque.ver_necessidade_pedidos', raise_exception=True)
def necessidade_pedidos(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', 'nome')
    direction = request.GET.get('direction', 'asc')

    # Filtro de busca por nome do produto
    produtos = Products.objects.filter(name__icontains=search_query)

    # Lista para armazenar as informações finais com pedidos separados e faltantes
    produtos_quantidades = []

    # Iterando pelos produtos para buscar os pedidos faltando separação
    for produto in produtos:
        faltando_separacao = FaltandoSeparacao.objects.filter(cod_produto=produto.product_code)
        pedidos_separados = faltando_separacao.aggregate(total_separado=Sum('quantidade_separada'))['total_separado'] or 0
        pedidos_faltando = faltando_separacao.aggregate(total_faltando=Sum(F('quantidade_pedido') - F('quantidade_separada')))['total_faltando'] or 0

        produtos_quantidades.append({
            'nome': produto.name,
            'pedidos_separados': pedidos_separados,
            'pedidos_faltando': pedidos_faltando,
        })

    # Ordenar a lista de produtos calculados
    reverse_order = (direction == 'desc')
    produtos_quantidades = sorted(produtos_quantidades, key=lambda x: x[order_by], reverse=reverse_order)

    context = {
        'produtos_quantidades': produtos_quantidades,
        'search_query': search_query,
        'order_by': order_by,
        'direction': direction,
    }

    return render(request, 'necessidade_pedidos.html', context)




@login_required
@permission_required('estoque.ver_estoque_por_lotes', raise_exception=True)
def estoque_lotes(request, lote):
    # Filtra os registros de estoque para o lote específico
    registros_estoque = Estoque.objects.filter(lote=lote)

    # Verifica se existem registros e tenta pegar o código do produto
    if registros_estoque.exists():
        produto_code = registros_estoque.first().cod_produto  # Acesse o primeiro registro
        nome_produto = Products.objects.filter(product_code=produto_code).first()
    else:
        produto_code = 'Produto não encontrado'
        nome_produto = 'Nome não disponível'  # Adicionando um valor padrão

    # Separar entradas e saídas (assumindo status=True para entrada e status=False para saída)
    entradas = registros_estoque.filter(status=True)
    saidas = registros_estoque.filter(status=False)

    # Adiciona os detalhes das entradas
    for entrada in entradas:
        if entrada.fonte:
            entrada.fonte_nome = entrada.fonte.__class__.__name__  # Obtém o nome da classe da fonte
            if isinstance(entrada.fonte, TransferenciaEstoqueSaidaInfo):
                entrada.fonte_id = entrada.fonte.numero_transferencia
                entrada.fonte_info = entrada.fonte.numero_transferencia
            elif isinstance(entrada.fonte, MistoItem):
                entrada.fonte_id = entrada.fonte.id  # ID do misto item
                entrada.fonte_info = entrada.fonte.name if hasattr(entrada.fonte, 'name') else 'Nome não disponível'
            else:
                entrada.fonte_nome = 'Fonte não encontrada'
                entrada.fonte_info = 'Nome não disponível'
        else:
            entrada.fonte_nome = 'Fonte não encontrada'
            entrada.fonte_id = None
            entrada.fonte_info = 'Nome não disponível'

    # Adiciona os detalhes das saídas
    for saida in saidas:
        if saida.fonte:
            saida.fonte_nome = saida.fonte.__class__.__name__  # Obtém o nome da classe da fonte
            if isinstance(saida.fonte, Pedido):
                saida.fonte_id = saida.fonte.id  # ID do pedido
                saida.fonte_info = saida.fonte.name if hasattr(saida.fonte, 'name') else 'Nome não disponível'
            elif isinstance(saida.fonte, MistoItem):
                saida.fonte_id = saida.fonte.id  # ID do misto item
                saida.fonte_info = saida.fonte.name if hasattr(saida.fonte, 'name') else 'Nome não disponível'
            else:
                saida.fonte_id = None
                saida.fonte_info = 'Fonte não reconhecida'
        else:
            saida.fonte_nome = 'Fonte não encontrada'
            saida.fonte_id = None
            saida.fonte_info = 'Nome não disponível'

    context = {
        'lote': lote,
        'produto': nome_produto,
        'entradas': entradas,
        'saidas': saidas,
        'detalhes': registros_estoque,
    }

    return render(request, 'estoque/estoque_lotes.html', context)

@login_required
@permission_required('estoque.ver_estoque_por_lotes', raise_exception=True)
def pesquisar_lote(request):
    if request.method == 'GET':
        return render(request, 'estoque/pesquisar_lote.html')

    if request.method == 'POST':
        lote = request.POST.get('lote', '')
        if lote:
            return estoque_lotes(request, lote)
        else:
            return render(request, 'estoque/pesquisar_lote.html', {'error': 'O campo de lote não pode estar vazio.'})
