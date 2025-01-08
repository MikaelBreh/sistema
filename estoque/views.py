from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Sum, F, Max, ExpressionWrapper
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from produtos_acabados.models import MistoItem, TransferenciaEstoqueSaidaInfo
from vendas.models import FaltandoSeparacao, PedidoItem, Pedido, PedidoSeparacao
from .models import Estoque, InventariosEstoque
from cadastros.models import Products, Products_another_info, KitItem


# @login_required
# @permission_required('estoque.view_estoque', raise_exception=True)
# def visualizar_estoque(request):
#     # Filtro de busca por nome do produto
#     search_query = request.GET.get('search', '')
#     show_only_necessity = request.GET.get('necessidade', False)
#     order_by = request.GET.get('order_by', 'nome')  # Valor padrão: 'nome'
#     direction = request.GET.get('direction', 'asc')  # Direção padrão: 'asc' (crescente)
#
#     # Definir a ordem de classificação com base na direção
#     if direction == 'desc':
#         order_by = f'-{order_by}'
#
#     # Filtrar produtos por nome
#     produtos = Products.objects.all()
#     if search_query:
#         produtos = produtos.filter(name__icontains=search_query)
#
#     # Filtra estoques para os produtos encontrados
#     estoques = Estoque.objects.filter(cod_produto__in=produtos.values('product_code'))
#
#     # Agrupamento e soma do estoque por produto
#     produtos_quantidades = estoques.values('cod_produto').annotate(
#         estoque_total=Sum('quantidade')
#     )
#
#     # Filtrar itens de pedido relacionados aos produtos
#     product_content_type = ContentType.objects.get_for_model(Products)
#     pedido_itens = PedidoItem.objects.filter(
#         content_type=product_content_type,
#         object_id__in=produtos.values('id'),
#         pedido__status__in=['aprovados', 'separando', 'separacao_finalizada']
#     ).values('object_id').annotate(pedidos_total=Sum('quantidade'))
#
#     # Dicionário de pedidos por produto
#     pedidos_por_produto = {
#         item['object_id']: item['pedidos_total']
#         for item in pedido_itens
#     }
#
#     # Agora buscamos o nome, estoque mínimo, e aplicamos o filtro de necessidade
#     produtos_detalhes = []
#     for produto in produtos_quantidades:
#         try:
#             produto_detalhe = Products.objects.get(product_code=produto['cod_produto'])
#             pedidos = pedidos_por_produto.get(produto_detalhe.id, 0)
#             estoque_apos_pedidos = produto['estoque_total'] - pedidos
#
#             # Verifica se o estoque é menor que o estoque mínimo (se a opção de necessidade for marcada)
#             if not show_only_necessity or (produto['estoque_total'] < produto_detalhe.estoq_minimo):
#                 produtos_detalhes.append({
#                     'nome': produto_detalhe.name,
#                     'estoque_minimo': produto_detalhe.estoq_minimo,
#                     'estoque_total': produto['estoque_total'],
#                     'pedidos': pedidos,
#                     'estoque_apos_pedidos': estoque_apos_pedidos,
#                 })
#         except Products.DoesNotExist:
#             pass
#
#     # Ordenação dos produtos de acordo com o parâmetro escolhido
#     produtos_detalhes = sorted(produtos_detalhes, key=lambda x: x[order_by.lstrip('-')], reverse=(direction == 'desc'))
#
#     # Paginação
#     page = request.GET.get('page', 1)
#     paginator = Paginator(produtos_detalhes, 10)
#     estoque_page = paginator.get_page(page)
#
#     context = {
#         'produtos_quantidades': estoque_page,
#         'search_query': search_query,
#         'show_only_necessity': show_only_necessity,
#         'estoque': estoque_page,
#         'order_by': order_by.lstrip('-'),  # Passa o campo de ordenação atual
#         'direction': direction,  # Passa a direção atual
#     }
#
#     return render(request, 'estoque/visualizar_estoque.html', context)
#

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
        pedidos_separados = faltando_separacao.aggregate(total_separado=Sum('quantidade_separada'))[
                                'total_separado'] or 0
        pedidos_faltando = \
            faltando_separacao.aggregate(total_faltando=Sum(F('quantidade_pedido') - F('quantidade_separada')))[
                'total_faltando'] or 0

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
            elif isinstance(entrada.fonte, InventariosEstoque):
                entrada.fonte_id = entrada.fonte.numero_inventario
                entrada.fonte_info = entrada.fonte.numero_inventario
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


@login_required()
@permission_required('inventariosestoque.ver_inventario_estoque', raise_exception=True)
def inventarios_estoque(request):
    Inventarios = InventariosEstoque.objects.all()

    inventarios_corrigidos = []
    numeros_adicionados = set()  # Para rastrear os números de inventário já adicionados

    for inventario in Inventarios:
        numero_inventario = inventario.numero_inventario
        finalizado = inventario.finalizado

        # Verifica se o número já foi adicionado
        if numero_inventario not in numeros_adicionados:
            # Conta os itens relacionados a este número de inventário
            quantidade_itens = InventariosEstoque.objects.filter(numero_inventario=numero_inventario).count()
            quantidade_produtos = \
                InventariosEstoque.objects.filter(numero_inventario=numero_inventario).values('quantidade').aggregate(
                    Sum('quantidade'))['quantidade__sum']

            # Adiciona os dados do inventário à lista corrigida
            inventarios_corrigidos.append([
                numero_inventario,
                inventario.conferente,
                inventario.data.strftime('%d/%m/%Y %H:%M'),
                quantidade_itens,  # Adiciona a quantidade de itens
                quantidade_produtos,
                finalizado,
            ])
            # Adiciona o número ao conjunto para evitar duplicatas
            numeros_adicionados.add(numero_inventario)

    print(inventarios_corrigidos)

    if request.method == 'GET':
        return render(request, 'estoque/inventarios_estoque.html', {'Inventarios': inventarios_corrigidos})


@login_required
@permission_required('inventariosestoque.editar_inventario_estoque', raise_exception=True)
def criar_inventario_estoque(request):
    Produtos = Products.objects.all()

    # Obter o maior valor de 'numero_inventario'
    ultimo_numero_inventario = InventariosEstoque.objects.aggregate(Max('numero_inventario'))['numero_inventario__max']

    if request.method == 'GET':
        return render(request, 'estoque/criar_inventario_estoque.html', {'Produtos': Produtos})

    if request.method == 'POST':
        numero_inventario = ultimo_numero_inventario + 1 if ultimo_numero_inventario else 1
        produto_input = request.POST.getlist('produto_input', '')
        cod_produtos = request.POST.getlist('codigo_produto')
        lotes = request.POST.getlist('lote')
        quantidades = request.POST.getlist('quantidade')

        # Usar o usuário autenticado como conferente
        conferente = request.user

        if cod_produtos and lotes and quantidades:
            for i in range(len(cod_produtos)):
                # Verifica se os campos individuais estão preenchidos
                if cod_produtos[i] and lotes[i] and quantidades[i]:
                    InventariosEstoque.objects.create(
                        numero_inventario=numero_inventario,
                        nome_produtos=produto_input[i],
                        cod_produto=cod_produtos[i],
                        lote=lotes[i],
                        quantidade=quantidades[i],
                        conferente=conferente
                    )
            return redirect('inventarios_estoque')

        error_message = "Todos os campos devem ser preenchidos para todos os produtos."
        return render(request, 'estoque/criar_inventario_estoque.html', {
            'Produtos': Produtos,
            'error_message': error_message,
        })

    return render(request, 'estoque/criar_inventario_estoque.html', {'Produtos': Produtos})


@login_required
@permission_required('inventariosestoque.ver_inventario_estoque', raise_exception=True)
def visualizar_inventario_estoque(request, inventario_id):
    Produtos = Products.objects.all()

    usuario_pode_editar = request.user.has_perm('inventariosestoque.editar_inventario_estoque')

    # Buscar os itens do inventário pelo ID
    inventario = InventariosEstoque.objects.filter(numero_inventario=inventario_id)

    if not inventario.exists():
        return redirect('inventarios_estoque')  # Redireciona caso o inventário não exista

    # Verificar se pelo menos uma das linhas está finalizada
    algum_finalizado = inventario.filter(finalizado=True).exists()

    if request.method == 'GET':
        return render(request, 'estoque/visualizar_inventario_estoque.html', {
            'Produtos': Produtos,
            'inventario': inventario,
            'numero_inventario': inventario_id,
            'algum_finalizado': algum_finalizado,
            'usuario_pode_editar': usuario_pode_editar,
        })

    if request.method == 'POST':
        # Alterar os itens do inventário para finalizado=True
        inventario.update(finalizado=True)

        # Transferir dados para a model Estoque
        estoque_entries = []
        for item in inventario:
            estoque_entries.append(Estoque(
                content_type=ContentType.objects.get_for_model(InventariosEstoque),
                object_id=item.id,
                cod_produto=item.cod_produto,
                lote=item.lote,
                quantidade=item.quantidade,
                status=True,  # Status como entrada
                inventario=True,
                id_inventario=inventario_id,
            ))

        # Salvar em lote para performance
        Estoque.objects.bulk_create(estoque_entries)

        messages.success(request, f'Inventário {inventario_id} finalizado e transferido para o estoque.')
        return redirect('inventarios_estoque')


@login_required
@permission_required('inventariosestoque.editar_inventario_estoque', raise_exception=True)
def editar_inventario_estoque(request, inventario_id):
    Produtos = Products.objects.all()

    # Buscar os itens do inventário pelo ID
    inventario = InventariosEstoque.objects.filter(numero_inventario=inventario_id)
    if not inventario.exists():
        return redirect('inventarios_estoque')  # Redireciona caso o inventário não exista

    # Verificar se pelo menos uma das linhas está finalizada
    algum_finalizado = inventario.filter(finalizado=True).exists()

    if algum_finalizado:
        return redirect('inventarios_estoque')

    if request.method == 'GET':
        return render(request, 'estoque/editar_inventario_estoque.html', {
            'Produtos': Produtos,
            'inventario': inventario,
            'numero_inventario': inventario_id,
        })

    if request.method == 'POST':
        produto_input = request.POST.getlist('produto_input', '')
        cod_produtos = request.POST.getlist('codigo_produto')
        lotes = request.POST.getlist('lote')
        quantidades = request.POST.getlist('quantidade')

        conferente = request.user

        # Excluir todos os registros existentes para o número do inventário
        InventariosEstoque.objects.filter(numero_inventario=inventario_id).delete()

        if cod_produtos and lotes and quantidades:
            for i in range(len(cod_produtos)):
                if cod_produtos[i] and lotes[i] and quantidades[i]:
                    InventariosEstoque.objects.create(
                        numero_inventario=inventario_id,
                        nome_produtos=produto_input[i],
                        cod_produto=cod_produtos[i],
                        lote=lotes[i],
                        quantidade=quantidades[i],
                        conferente=conferente
                    )
            return redirect('inventarios_estoque')

        error_message = "Todos os campos devem ser preenchidos para todos os produtos."
        return render(request, 'estoque/editar_inventario_estoque.html', {
            'Produtos': Produtos,
            'inventario': inventario,
            'numero_inventario': inventario_id,
            'error_message': error_message,
        })


# -------------  Nova VIEW do estoque ------------------
@login_required
@permission_required('estoque.view_estoque', raise_exception=True)
def nova_view_estoque(request):
    search_query = request.GET.get('search', '')
    show_only_necessity = request.GET.get('necessidade', False)
    order_by = request.GET.get('order_by', 'nome')  # Valor padrão: 'nome'
    direction = request.GET.get('direction', 'asc')  # Direção padrão: 'asc' (crescente)

    if direction == 'desc':
        order_by = f'-{order_by}'

    produtos = Products.objects.all()
    if search_query:
        produtos = produtos.filter(name__icontains=search_query)

    # Obter os inventários mais recentes por produto
    inventarios = Estoque.objects.filter(inventario=True).values('cod_produto', 'id_inventario').annotate(
        ultimo_inventario=Max('data'),
        soma_inventario=Sum('quantidade')  # Soma as quantidades dos inventários com o mesmo `id_inventario`
    )

    # Transformar inventários em um dicionário para fácil acesso
    inventarios_dict = {
        inv['cod_produto']: {
            'ultimo_inventario': inv['ultimo_inventario'],
            'soma_inventario': inv['soma_inventario'],
        }
        for inv in inventarios
    }

    print(inventarios_dict)

    # Filtrar estoques pelos produtos selecionados
    estoques = Estoque.objects.filter(
        cod_produto__in=produtos.values('product_code')
    )

    # Criar lista de estoques filtrados considerando as regras do inventário
    estoques_filtrados = []
    for estoque in estoques:
        inventario_info = inventarios_dict.get(estoque.cod_produto)
        if inventario_info:
            ultimo_inventario = inventario_info['ultimo_inventario']
            # Considerar apenas entradas/saídas após o último inventário
            if estoque.data > ultimo_inventario:
                print(estoque.data, ultimo_inventario)
                estoques_filtrados.append(estoque)
        else:
            # Caso o produto não tenha inventário, incluir normalmente
            estoques_filtrados.append(estoque)

    print(estoques_filtrados)

    # Calcular o estoque final, começando pela soma dos inventários
    estoque_agrupado = {
        cod_produto: info['soma_inventario']
        for cod_produto, info in inventarios_dict.items()
    }

    # Adicionar entradas/saídas após o inventário
    for estoque in estoques_filtrados:
        estoque_agrupado[estoque.cod_produto] = (
                estoque_agrupado.get(estoque.cod_produto, 0) + estoque.quantidade
        )

    # Dicionário para armazenar componentes de kits
    componentes_kits = {}

    # Calcular componentes dos kits a partir de PedidoItem
    pedidos_separar_geral = PedidoItem.objects.filter(
        content_type=ContentType.objects.get_for_model(Products)
    ).exclude(
        separacoes__isnull=False
    ).exclude(
        pedido__status='em_aberto'
    )

    for pedido_item in pedidos_separar_geral:
        produto = Products.objects.get(id=pedido_item.object_id)

        if produto.category == 'kit':  # Verificar se o produto é um kit
            itens_kit = KitItem.objects.filter(produto_kit=produto)
            for item in itens_kit:
                # Calcular a quantidade necessária do componente
                quantidade_componente = int(pedido_item.quantidade * item.quantidade)  # Transformar em inteiro
                if item.produto_componente.name in componentes_kits:
                    componentes_kits[item.produto_componente.name] += quantidade_componente
                else:
                    componentes_kits[item.produto_componente.name] = quantidade_componente

    # Calcular componentes dos kits a partir de FaltandoSeparacao
    faltando_separacoes = FaltandoSeparacao.objects.all()

    for faltando in faltando_separacoes:
        quantidade_faltante = faltando.quantidade_pedido - faltando.quantidade_separada

        # Verificar se o item faltante pertence a um kit
        produto = Products.objects.get(id=faltando.item_pedido.object_id)
        if produto.category == 'kit':  # Verificar se o produto é um kit
            itens_kit = KitItem.objects.filter(produto_kit=produto)
            for item in itens_kit:
                # Calcular a quantidade necessária do componente
                quantidade_componente = int(quantidade_faltante * item.quantidade)  # Transformar em inteiro
                if item.produto_componente.name in componentes_kits:
                    componentes_kits[item.produto_componente.name] += quantidade_componente
                else:
                    componentes_kits[item.produto_componente.name] = quantidade_componente

    # Detalhes de produtos
    produtos_detalhes = []
    for produto in produtos:
        estoque_total = estoque_agrupado.get(produto.product_code, 0)
        produtos_relacionados = Products_another_info.objects.filter(produto_pertence=produto)
        for produto_relacionado in produtos_relacionados:
            estoque_total += estoque_agrupado.get(produto_relacionado.product_code, 0)

        produto_content_type = ContentType.objects.get_for_model(produto)

        quantidade_separada = PedidoSeparacao.objects.filter(
            item_pedido__content_type=produto_content_type,
            item_pedido__object_id=produto.id
        ).exclude(
            pedido__status='finalizados'
        ).aggregate(total=Sum('quantidade'))['total'] or 0

        for produto_relacionado in produtos_relacionados:
            produto_relacionado_content_type = ContentType.objects.get_for_model(produto_relacionado)
            quantidade_separada += PedidoSeparacao.objects.filter(
                item_pedido__content_type=produto_relacionado_content_type,
                item_pedido__object_id=produto_relacionado.id
            ).exclude(
                pedido__status='finalizados'
            ).aggregate(total=Sum('quantidade'))['total'] or 0



        # coluna Pedidos Separar - pedidos que ainda faltam separar
        pedidos_separar = PedidoItem.objects.filter(
            content_type=produto_content_type,
            object_id=produto.id
        ).exclude(
            separacoes__isnull=False
        ).exclude(
            pedido__status='em_aberto'
        ).exclude(
            pedido__status='separando'
        ).exclude(
            pedido__status='separacao_finalizada'
        ).exclude(
            pedido__status='conf_separacao'
        ).exclude(
            pedido__status='finalizados'
        ).aggregate(total=Sum('quantidade'))['total'] or 0

        # Calcular quantidade faltante a separar
        faltando_separar = FaltandoSeparacao.objects.filter(
            item_pedido__content_type=produto_content_type,
            item_pedido__object_id=produto.id
        ).exclude(
            pedido__status='finalizados'
        ).annotate(
            quantidade_faltante=F('quantidade_pedido') - F('quantidade_separada')
        ).aggregate(
            total_faltante=Sum('quantidade_faltante')
        )['total_faltante'] or 0

        # Adicionar aos pedidos a separar
        pedidos_separar += faltando_separar

        for produto_relacionado in produtos_relacionados:
            produto_relacionado_content_type = ContentType.objects.get_for_model(produto_relacionado)
            pedidos_separar += PedidoItem.objects.filter(
                content_type=produto_relacionado_content_type,
                object_id=produto_relacionado.id
            ).exclude(
                separacoes__isnull=False
            ).exclude(
                pedido__status='em_aberto'
            ).aggregate(total=Sum('quantidade'))['total'] or 0

            # Fim da coluna Pedidos Separar



        # Estoque virtual (incluindo o desconto dos componentes dos kits)
        estoque_virtual = estoque_total - (quantidade_separada + pedidos_separar + componentes_kits.get(produto.name, 0))

        if not show_only_necessity or estoque_virtual < produto.estoq_minimo:
            produtos_detalhes.append({
                'codigo': produto.product_code,
                'nome': produto.name,
                'estoque_minimo': produto.estoq_minimo,
                'estoque_total': estoque_total,
                'quantidade_separada': quantidade_separada,
                'pedidos_separar': pedidos_separar,
                'estoque_virtual': estoque_virtual,
                'componentes_kits': componentes_kits.get(produto.name, 0),  # Adicionar os componentes do kit
            })

    produtos_detalhes = sorted(produtos_detalhes, key=lambda x: x[order_by.lstrip('-')],
                               reverse=(direction == 'desc'))

    page = request.GET.get('page', 1)
    paginator = Paginator(produtos_detalhes, 20)
    estoque_page = paginator.get_page(page)

    context = {
        'produtos_quantidades': estoque_page,
        'search_query': search_query,
        'show_only_necessity': show_only_necessity,
        'estoque': estoque_page,
        'order_by': order_by.lstrip('-'),
        'direction': direction,
    }

    return render(request, 'estoque/visualizar_novo_estoque.html', context)


def detalhar_quantidade_separada(request, product_code):
    # Obter o produto principal pelo código
    produto = get_object_or_404(Products, product_code=product_code)

    # Obter os produtos relacionados
    produtos_relacionados = Products_another_info.objects.filter(produto_pertence=produto)

    # Inicializar lista de detalhes
    detalhes_separados = []

    # Obter content type do produto
    produto_content_type = ContentType.objects.get_for_model(produto)

    # Buscar separações para o produto principal
    separacoes = PedidoSeparacao.objects.filter(
        item_pedido__content_type=produto_content_type,
        item_pedido__object_id=produto.id
    ).exclude(
        pedido__status='finalizados'
    )

    # Adicionar detalhes do produto principal
    for separacao in separacoes:
        detalhes_separados.append({
            'pedido_id': separacao.pedido.id,
            'pedido_nome': str(separacao.pedido),
            'cliente': separacao.pedido.cliente.name,
            'lote': separacao.lote,
            'quantidade': separacao.quantidade,
            'data_pedido': separacao.pedido.data,
            'status_pedido': separacao.pedido.status,
        })

    # Buscar separações para os produtos relacionados
    for produto_relacionado in produtos_relacionados:
        produto_relacionado_content_type = ContentType.objects.get_for_model(produto_relacionado)
        separacoes_relacionadas = PedidoSeparacao.objects.filter(
            item_pedido__content_type=produto_relacionado_content_type,
            item_pedido__object_id=produto_relacionado.id
        ).exclude(
            pedido__status='finalizados'
        )
        for separacao in separacoes_relacionadas:
            detalhes_separados.append({
                'pedido_id': separacao.pedido.id,
                'pedido_nome': str(separacao.pedido),
                'cliente': separacao.pedido.cliente.name,
                'lote': separacao.lote,
                'quantidade': separacao.quantidade,
                'data_pedido': separacao.pedido.data,
                'status_pedido': separacao.pedido.status,
            })

    # Passar os detalhes para o template
    context = {
        'produto': produto,
        'detalhes_separados': detalhes_separados,
    }
    return render(request, 'estoque/detalhar_quantidade_separada.html', context)



def detalhar_pedidos_separar(request, product_code):
    # Obter o produto principal pelo código
    produto = get_object_or_404(Products, product_code=product_code)

    # Obter os produtos relacionados
    produtos_relacionados = Products_another_info.objects.filter(produto_pertence=produto)

    # Inicializar lista de detalhes
    detalhes_pedidos = []

    # Obter content type do produto
    produto_content_type = ContentType.objects.get_for_model(produto)

    # Buscar pedidos a separar para o produto principal
    pedidos = PedidoItem.objects.filter(
        content_type=produto_content_type,
        object_id=produto.id
    ).exclude(
        separacoes__isnull=False
    ).exclude(
        pedido__status='em_aberto'
    ).exclude(
        pedido__status='separando'
    ).exclude(
        pedido__status='separacao_finalizada'
    ).exclude(
        pedido__status='conf_separacao'
    ).exclude(
        pedido__status='finalizados'
    )

    # Obter separações parcialmente feitas para o produto principal
    pedidos_parcialmente_separados = FaltandoSeparacao.objects.filter(
        item_pedido__content_type=produto_content_type,
        item_pedido__object_id=produto.id
    )



    # Adicionar detalhes do produto principal
    for pedido_item in pedidos:
        detalhes_pedidos.append({
            'pedido_id': pedido_item.pedido.id,
            'pedido_nome': str(pedido_item.pedido),
            'cliente': pedido_item.pedido.cliente.name,
            'quantidade': pedido_item.quantidade,
            'data_pedido': pedido_item.pedido.data,
            'status_pedido': pedido_item.pedido.status,
        })

    # Adicionar detalhes dos pedidos parcialmente separados
    for item in pedidos_parcialmente_separados:

        quantidade_calculada = item.quantidade_pedido - item.quantidade_separada

        detalhes_pedidos.append({
            'pedido_id': item.pedido.id,
            'pedido_nome': str(item.pedido),
            'cliente': item.pedido.cliente.name,
            'quantidade': quantidade_calculada,
            'data_pedido': item.pedido.data,
            'status_pedido': item.pedido.status,
        })


    # Buscar pedidos a separar para os produtos relacionados
    for produto_relacionado in produtos_relacionados:
        produto_relacionado_content_type = ContentType.objects.get_for_model(produto_relacionado)
        pedidos_relacionados = PedidoItem.objects.filter(
            content_type=produto_relacionado_content_type,
            object_id=produto_relacionado.id
        ).exclude(
            separacoes__isnull=False
        ).exclude(
            pedido__status='em_aberto'
        )
        for pedido_item in pedidos_relacionados:
            detalhes_pedidos.append({
                'pedido_id': pedido_item.pedido.id,
                'pedido_nome': str(pedido_item.pedido),
                'cliente': pedido_item.pedido.cliente.name,
                'quantidade': pedido_item.quantidade,
                'data_pedido': pedido_item.pedido.data,
                'status_pedido': pedido_item.pedido.status,
            })

    # Passar os detalhes para o template
    context = {
        'produto': produto,
        'detalhes_pedidos': detalhes_pedidos,
    }
    return render(request, 'estoque/detalhar_pedidos_separar.html', context)












