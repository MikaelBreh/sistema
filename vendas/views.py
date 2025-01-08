from datetime import datetime
from itertools import chain

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from cadastros.models import Clientes, Products, TabelaPrecoProduto, Products_another_info

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from estoque.models import Estoque
from .functions.validar_separacao import validar_lote
from .models import Pedido, PedidoItem, PedidoSeparacao, FaltandoSeparacao, SaidaPedido
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F

from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@login_required
def home(request):
    if request.method == 'GET':
        nomes_clientes = Clientes.objects.all()
        return render(request, 'vendas/home.html', {'clientes': nomes_clientes})


@login_required
def get_produtos_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    tabela_preco = cliente.TabelaPreco
    produtos_tabela = TabelaPrecoProduto.objects.filter(tabela_preco=tabela_preco).select_related('produto')
    produtos_data = [{'id': p.produto.id, 'nome': p.produto.name, 'preco': p.valor_sem_impostos} for p in
                     produtos_tabela]
    print(produtos_data)
    return JsonResponse(produtos_data, safe=False)


@login_required
def listar_pedidos(request, *args, **kwargs):
    opcao = kwargs.get('opcao')
    search_query = request.GET.get('search', '')
    if search_query:
        pedidos = Pedido.objects.filter(
            Q(cliente__name__icontains=search_query) & Q(aprovado=False)
        )
    else:
        pedidos = Pedido.objects.filter(aprovado=False)

    paginator = Paginator(pedidos, 10)  # Mostra 40 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendas/listagem_pedidos.html', {'pedidos': page_obj, 'opcao': opcao})


@login_required
@permission_required('vendas.add_pedido', raise_exception=True)
def criar_pedido_separacao(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Clientes, id=cliente_id)

        quantidade_caixas_total = request.POST.getlist('quant_caixas_total')
        regime_venda = request.POST.get('regime_input')
        pedido = Pedido.objects.create(
            cliente=cliente,
            regime_venda=regime_venda,
            quantidade_inicial_caixas=int(quantidade_caixas_total[0]),
        )

        produtos = request.POST.getlist('nome_produto')
        quantidades = request.POST.getlist('quantidade_produto')
        quantidades_caixas = request.POST.getlist('quantidade_caixas')

        for produto, quantidade, quantidade_caixa in zip(produtos, quantidades, quantidades_caixas):
            content_type = None
            object_id = None

            # Verificar se o produto está na primeira tabela
            produto_obj = Products.objects.filter(name=produto).first()
            if produto_obj:
                content_type = ContentType.objects.get_for_model(Products)
                object_id = produto_obj.id
            else:
                # Verificar se o produto está na segunda tabela
                produto_obj = Products_another_info.objects.filter(name=produto).first()
                if produto_obj:
                    content_type = ContentType.objects.get_for_model(Products_another_info)
                    object_id = produto_obj.id

            try:

                if content_type and object_id:
                    quantidade_caixa_correta = int(float(quantidade_caixa))

                    PedidoItem.objects.create(
                        pedido=pedido,
                        content_type=content_type,
                        object_id=object_id,
                        quantidade=quantidade,
                        quantidade_caixas=quantidade_caixa_correta
                    )

            except Exception as e:
                print(e)
                return HttpResponse("Erro ao criar pedido")

        return redirect('listar_pedidos')



    else:
        nomes_clientes_all = Clientes.objects.all()
        nome_produtos_all = list(chain(Products.objects.all(), Products_another_info.objects.all()))
        user_criar_amostra = request.user.has_perm('Pedido.criar_pedido_amostra')

        return render(request, 'vendas/criar_pedido_separacao.html',
                      {'clientes': nomes_clientes_all, 'produtos': nome_produtos_all, 'user_criar_amostra': user_criar_amostra})


@login_required
def visualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    itens_pedido = PedidoItem.objects.filter(pedido=pedido)
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido)

    # Carregar os objetos relacionados para cada item do pedido
    for item in itens_pedido:
        content_type = ContentType.objects.get_for_id(item.content_type_id)
        model_class = content_type.model_class()
        item.product_instance = model_class.objects.get(id=item.object_id)

    return render(request, 'vendas/visualizar_pedido.html',
                  {'pedido': pedido, 'itens_pedido': itens_pedido, 'separacoes': separacoes})


@login_required
def imprimir_conferencia(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    itens_pedido = PedidoItem.objects.filter(pedido=pedido)
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido)

    # Carregar o objeto relacionado para cada item do pedido, adicionando o product_instance
    for item in itens_pedido:
        content_type = ContentType.objects.get_for_id(item.content_type_id)
        model_class = content_type.model_class()
        item.product_instance = model_class.objects.get(id=item.object_id)

    # Gerar o PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Conferência do Pedido {pedido.id}")

    pdf.setFont("Helvetica", 30)
    pdf.drawString(145, 650, "Conferência de Pedido")

    pdf.setFont("Helvetica", 12)
    # Cabeçalho do PDF
    pdf.drawString(100, 750, f"Pedido ID: {pedido.id}")
    pdf.drawString(320, 750, f"Cliente: {pedido.cliente.name}")
    pdf.drawString(320, 735, f"Data do Pedido: {pedido.data.strftime('%d/%m/%Y - %H:%M')}")
    pdf.drawString(100, 735, f"Status: {pedido.status}")

    pdf.line(100, 700, 500, 700)

    # Tabela dos itens
    y_position = 590
    pdf.drawString(60, y_position, "Produto")
    pdf.drawString(380, y_position, "Caixas")
    pdf.drawString(440, y_position, "Lote")

    y_position -= 20
    y_position -= 20  # Definindo a posição vertical inicial

    soma_caixas_total = 0
    soma_peso_liquido_total = 0
    soma_peso_bruto_total = 0

    # Exibir total de caixas separadas
    for item in itens_pedido:
        # Soma total da quantidade separada para o item atual
        total_separado = sum(separacao.quantidade for separacao in item.separacoes.all())

        # Calcula o número de caixas separadas dividindo pela quantidade de produtos por caixa
        total_caixas_separadas = total_separado / item.product_instance.box_quantity

        soma_peso_liquido_total += total_separado * item.product_instance.net_weight
        soma_peso_bruto_total += total_separado * item.product_instance.gross_weight

        soma_caixas_total += total_caixas_separadas

        # Exibe o nome do produto e a quantidade de caixas separadas no PDF
        pdf.drawString(60, y_position, item.product_instance.name)
        pdf.drawString(385, y_position, f"  {str(int(total_caixas_separadas))} (  ) ")

        # Exibe os lotes usados
        lotes = ", ".join([separacao.lote for separacao in item.separacoes.all() if separacao.lote])
        pdf.drawString(440, y_position, lotes if lotes else "Sem lote")

        # Movendo para a próxima linha no PDF
        y_position -= 20

        # Adicionando uma nova página se a posição estiver muito baixa
        if y_position < 100:
            pdf.showPage()
            y_position = 750  # Resetando a posição para o topo da nova página

    # Exibir o total de caixas separadas
    pdf.drawString(60, y_position - 80, f"Total de caixas: {int(soma_caixas_total)}  (  )       "
                                        f" Peso Liquido: {int(soma_peso_liquido_total)} KG       Peso Bruto: {int(soma_peso_bruto_total)} KG")
    pdf.drawString(60, y_position - 130,
                   "Nome Conferente: _______________    Assinatura do conferente:  ____________________")
    pdf.drawString(60, y_position - 180,
                   "Separado Por: __________________    Assinatura do separador:  _____________________")

    pdf.save()
    buffer.seek(0)

    # Retornar o PDF como resposta
    return FileResponse(buffer, as_attachment=True, filename=f"Conferencia_Pedido_{pedido.id}.pdf")


@login_required
@permission_required('vendas.change_pedido', raise_exception=True)
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        # Atualiza o cliente do pedido
        cliente_id = request.POST.get('cliente_id')
        quantidade_total_caixas = request.POST.get('quant_caixas_total')

        cliente = get_object_or_404(Clientes, id=cliente_id)
        pedido.cliente = cliente
        pedido.quantidade_inicial_caixas = int(quantidade_total_caixas)
        pedido.save()

        # Obtém os produtos e quantidades enviados no form
        produtos = request.POST.getlist('nome_produto')
        quantidades = request.POST.getlist('quantidade_produto')
        quantidades_caixas = request.POST.getlist('quantidade_caixas')

        # Itera sobre os itens de pedido atuais
        itens_existentes = {item.id: item for item in PedidoItem.objects.filter(pedido=pedido)}

        for produto, quantidade, quantidade_caixa in zip(produtos, quantidades, quantidades_caixas):
            content_type = None
            object_id = None

            produto_obj = Products.objects.filter(name=produto).first()
            if produto_obj:
                content_type = ContentType.objects.get_for_model(Products)
                object_id = produto_obj.id
            else:
                produto_obj = Products_another_info.objects.filter(name=produto).first()
                if produto_obj:
                    content_type = ContentType.objects.get_for_model(Products_another_info)
                    object_id = produto_obj.id

            # Verifica se o item já existe para atualizar
            if content_type and object_id:
                quantidade_caixa_correta = int(float(quantidade_caixa))

                # Tenta localizar o item de pedido já existente
                item_existente = PedidoItem.objects.filter(
                    pedido=pedido,
                    content_type=content_type,
                    object_id=object_id
                ).first()

                # Se o item já existir, atualiza apenas se não houver separação associada
                if item_existente:
                    if PedidoSeparacao.objects.filter(item_pedido=item_existente).exists():
                        # Não pode editar se houver separação associada
                        continue
                    else:
                        # Atualiza o item existente
                        item_existente.quantidade = quantidade
                        item_existente.quantidade_caixas = quantidade_caixa_correta
                        item_existente.save()

                        # Remove dos itens existentes para manter o controle
                        itens_existentes.pop(item_existente.id, None)
                else:
                    # Se o item não existir, cria um novo
                    PedidoItem.objects.create(
                        pedido=pedido,
                        content_type=content_type,
                        object_id=object_id,
                        quantidade=quantidade,
                        quantidade_caixas=quantidade_caixa_correta
                    )

        # Remover os itens que não foram incluídos no novo pedido (não estão mais na lista)
        for item_id, item in itens_existentes.items():
            if not PedidoSeparacao.objects.filter(item_pedido=item).exists():
                item.delete()

        return redirect('listar_pedidos')

    else:

        nomes_clientes_all = Clientes.objects.all()
        nome_produtos_all = list(chain(Products.objects.all(), Products_another_info.objects.all()))
        itens_pedido = PedidoItem.objects.filter(pedido=pedido)

        # Carregar instâncias do produto para cada item de pedido
        for item in itens_pedido:
            content_type = ContentType.objects.get_for_id(item.content_type_id)
            model_class = content_type.model_class()
            item.product_instance = model_class.objects.get(id=item.object_id)

        # Pega os itens que possuem separações associadas
        itens_com_separacao = PedidoItem.objects.filter(pedido=pedido, separacoes__isnull=False).values_list('id',
                                                                                                             flat=True)

        return render(request, 'vendas/editar_pedido.html',
                      {'pedido': pedido, 'clientes': nomes_clientes_all, 'produtos': nome_produtos_all,
                       'itens_pedido': itens_pedido, 'itens_com_separacao': list(itens_com_separacao)})


def lancar_itens_no_estoque(pedido):
    # Obter o ContentType do modelo Pedido
    pedido_content_type = ContentType.objects.get_for_model(Pedido)

    # Filtrar as separações relacionadas ao pedido
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido)

    for separacao in separacoes:
        # Criar a entrada de saída de estoque, associando ao pedido como fonte
        Estoque.objects.create(
            content_type=separacao.item_pedido.content_type,  # Tipo do produto
            object_id=separacao.item_pedido.object_id,  # ID do produto
            cod_produto=separacao.item_pedido.produto.product_code,  # Código do produto
            lote=separacao.lote,  # Lote do produto
            quantidade=-separacao.quantidade,  # Quantidade negativa para representar a saída
            status=False,  # Definir como saída (False)
            fonte=pedido,  # Associar o pedido como fonte da saída
        )


def remover_itens_do_estoque(pedido):
    # Obter o ContentType do modelo Pedido
    pedido_content_type = ContentType.objects.get_for_model(Pedido)

    # Excluir todas as entradas no estoque onde o pedido é a fonte
    Estoque.objects.filter(
        content_type=pedido_content_type,  # Tipo do modelo é Pedido
        object_id=pedido.id  # ID do pedido
    ).delete()


@login_required
@permission_required('vendas.alterar_status', raise_exception=True)
def alterar_status(request, numero_pedido, novo_status):
    # Obter o pedido
    pedido = get_object_or_404(Pedido, id=numero_pedido)
    pedido_separacao = PedidoSeparacao.objects.filter(pedido=pedido)

    # Verifica o status anterior antes de alterar
    status_anterior = pedido.status

    # Nao permitir alterar o status para 'separando' ou outros status acima desse se o pedido nao tiver itens separados
    if novo_status != 'aprovados' and novo_status != 'em_aberto':
        if not pedido_separacao:
            messages.error(request, 'Não é possível alterar o status para Separando ou superiores por que o pedido não '
                                    'tem uma separação.')
            return redirect('listar_pedidos')

    # Alterar o status do pedido
    pedido.status = novo_status
    pedido.save()

    # Caso o pedido seja movido como finalizado, deve ser removidas as faltas das separacoes relacionadas ao pedido
    if novo_status != 'separacao_finalizada' or novo_status != 'finalizados':
        # Remover todos os itens da model FaltandoSeparacao relacionados ao pedido
        FaltandoSeparacao.objects.filter(pedido=pedido).delete()

    # Caso o pedido seja movido para cancelado, deve ser removidas as separacoes e faltas relacionadas ao pedido
    if novo_status == 'cancelado':
        # Remover todas as separações relacionadas ao pedido
        PedidoSeparacao.objects.filter(pedido=pedido).delete()

        # Remover todos os itens da model FaltandoSeparacao relacionados ao pedido
        FaltandoSeparacao.objects.filter(pedido=pedido).delete()

    # Lançar ou remover os itens no estoque dependendo do status
    if status_anterior != 'finalizados' and novo_status == 'finalizados':
        # O pedido está sendo finalizado, lança os itens no estoque
        lancar_itens_no_estoque(pedido)

        # Remover todos os itens da model FaltandoSeparacao relacionados ao pedido
        FaltandoSeparacao.objects.filter(pedido_id=pedido).delete()

        # redirecionar para a tela de lançar saida com base no id do pedido
        return redirect('lancar_saida', pedido_id=pedido.id)


    elif status_anterior == 'finalizados' and novo_status != 'finalizados':
        messages.error(request, 'Não é possível alterar o status de Finalizado pois o pedido esta encerrado.')
        return redirect('listar_pedidos')

    # Armazenar o novo status na sessão para garantir que a aba correta seja selecionada após o redirecionamento
    request.session['status_atual'] = novo_status

    # Redirecionar para a lista de pedidos com o status atualizado
    return redirect('listar_pedidos')


@login_required
@permission_required('vendas.view_pedido', raise_exception=True)
def listar_pedidos(request):
    # Recuperar o status atual da sessão, ou usar 'em_aberto' como padrão
    status_atual = request.session.get('status_atual', 'em_aberto')
    return render(request, 'pedidos/lista_pedidos.html', {'status_atual': status_atual})


@login_required
def listar_pedidos_por_status(request, status):
    busca = request.GET.get('busca', '')
    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')
    page = request.GET.get('page', 1)

    if status == 'todos':
        pedidos = Pedido.objects.all()
        print(pedidos)

    else:
        # Filtro básico por status
        pedidos = Pedido.objects.filter(status=status)

    # Filtros de busca
    if busca:
        pedidos = pedidos.filter(Q(id__icontains=busca) | Q(cliente__name__icontains=busca))

    # Filtro por intervalo de data
    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
        pedidos = pedidos.filter(data__gte=data_inicial)

    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d')
        pedidos = pedidos.filter(data__lte=data_final)

    # Paginação
    paginator = Paginator(pedidos, 60)  # 40 itens por página
    paginated_pedidos = paginator.get_page(page)

    # Preparando os dados para enviar via JSON
    pedidos_data = [
        {
            'numero_pedido': pedido.id,
            'cliente': pedido.cliente.name,
            'regime_venda': pedido.regime_venda,
            'data': pedido.data.strftime('%d/%m/%Y'),
        } for pedido in paginated_pedidos
    ]

    paginacao_data = {
        'num_pages': paginator.num_pages,
        'current_page': paginated_pedidos.number,
    }

    return JsonResponse({'pedidos': pedidos_data, 'paginacao': paginacao_data})


# EXPEDICAO -- AQUI COMECA A PARTE DA SEPARACAO DE PEDIDOS


@login_required
@permission_required('vendas.listar_pedidos_separacao', raise_exception=True)
def expedicao_list(request, status):
    search_query = request.GET.get('search', '')

    # Filtra os pedidos pelo status
    if status == 'aprovados':
        pedidos = Pedido.objects.filter(status='aprovados')
    elif status == 'separando':
        pedidos = Pedido.objects.filter(status='separando')
    elif status == 'separacao_finalizada':
        pedidos = Pedido.objects.filter(status='separacao_finalizada')
    else:
        pedidos = Pedido.objects.none()  # Caso de status inválido

    # Aplica filtro de busca, se houver
    if search_query:
        pedidos = pedidos.filter(cliente__name__icontains=search_query)

    # Se o usuário não é admin, mostra apenas os pedidos sem responsável ou atribuídos a ele
    if not request.user.is_superuser:
        pedidos = pedidos.filter(Q(usuario_responsavel=request.user) | Q(usuario_responsavel__isnull=True))

    paginator = Paginator(pedidos, 10)  # Mostra 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendas/expedicao_list.html', {'pedidos': page_obj, 'status': status})


@login_required
@permission_required('vendas.listar_pedidos_separacao', raise_exception=True)
def expedicao_separando_list_view(request):
    search_query = request.GET.get('search', '')

    if search_query:
        pedidos = Pedido.objects.filter(
            Q(cliente__name__icontains=search_query) &
            Q(status='separando')
        )
    else:
        pedidos = Pedido.objects.filter(
            Q(status='separando')
        )

    paginator = Paginator(pedidos, 10)  # Mostra 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendas/expedicao_list.html', {'pedidos': page_obj})


@login_required
@permission_required('vendas.view_pedidoseparacao', raise_exception=True)
def expedicao_ver_separacao(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido)

    return render(request, 'vendas/expedicao_ver_separacao.html', {
        'pedido': pedido,
        'separacoes': separacoes
    })


@login_required
@permission_required('vendas.change_pedidoseparacao', raise_exception=True)
def expedicao_separar_editar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido).select_related('item_pedido')

    if request.method == 'POST':
        is_finalizar = 'finalizar_pedido' in request.POST  # Checa se o pedido é para finalizar

        try:
            # Verifica o status do pedido e atualiza para 'separando' se necessário
            if pedido.status != 'separando':
                pedido.status = 'separando'
                pedido.usuario_responsavel = request.user  # Atribui o usuário atual como responsável
                pedido.save()

            for item in pedido.itens.all():
                lotes = request.POST.getlist(f'lotes_{item.id}')
                quantidades = request.POST.getlist(f'quantidades_{item.id}')

                # Excluir todas as separações anteriores desse item
                PedidoSeparacao.objects.filter(pedido=pedido, item_pedido=item).delete()

                total_quantidade = 0  # Controle do total de quantidades para cada item

                for lote, quantidade in zip(lotes, quantidades):
                    if lote and quantidade:
                        try:
                            # Valida o lote e o produto correspondente
                            lote_produto = validar_lote(lote, item)
                        except ValueError as e:
                            # Adiciona a mensagem de erro
                            messages.error(request, str(e))
                            # Recarrega a página com a mensagem de erro
                            return render(request, 'vendas/expedicao_separar_editar.html', {
                                'pedido': pedido,
                                'separacoes': separacoes,
                            })

                        # Acumula a quantidade separada
                        quantidade_int = int(quantidade)
                        total_quantidade += quantidade_int

                        if total_quantidade > item.quantidade:
                            raise ValidationError(
                                f"A quantidade separada para {item.produto.name} excede a quantidade do pedido."
                            )

                        # Salvar as novas separações
                        PedidoSeparacao.objects.create(
                            pedido=pedido,
                            item_pedido=item,
                            quantidade=quantidade_int,
                            lote=lote
                        )

                # Atualiza ou cria a entrada na model FaltandoSeparacao
                FaltandoSeparacao.objects.update_or_create(
                    pedido=pedido,
                    item_pedido=item,
                    defaults={
                        'cod_produto': item.produto.product_code,
                        'quantidade_pedido': item.quantidade,
                        'quantidade_separada': total_quantidade,
                    }
                )

                # Verifica se a ação é para finalizar e atualiza o status para 'conf_separacao'
                if is_finalizar:
                    pedido.status = 'conf_separacao'
                    pedido.save()

                    # Adiciona mensagem de sucesso e redireciona
                    return redirect('expedicao_list', status='separando')

            # Adiciona mensagem de sucesso e redireciona
            messages.success(request, 'Separação do pedido atualizada com sucesso.')


        except ValidationError as e:
            messages.error(request, str(e))

    # Renderiza a página caso não seja uma requisição POST ou haja um erro
    return render(request, 'vendas/expedicao_separar_editar.html', {
        'pedido': pedido,
        'separacoes': separacoes,
    })


@login_required
@permission_required('vendas.view_pedidoseparacao', raise_exception=True)
def ver_faltas_pedidos(request):
    # Consulta todos os itens que estão com falta na separação
    faltas = FaltandoSeparacao.objects.filter(quantidade_pedido__gt=F('quantidade_separada'))
    print(faltas)

    # Cria um dicionário que agrupa os itens por código de produto
    produtos_faltantes = {}
    for falta in faltas:
        falta_qtd = falta.quantidade_pedido - falta.quantidade_separada

        # Tenta pegar o produto a partir do código no modelo Products
        produto = Products.objects.filter(product_code=falta.cod_produto).first()

        # Se o produto não for encontrado no Products, tenta no Products_another_info
        if not produto:
            produto_another_info = Products_another_info.objects.filter(product_code=falta.cod_produto).first()
            if produto_another_info:
                produto = produto_another_info.produto_pertence  # Pega o produto associado no modelo Products

        # Se o produto for encontrado em qualquer um dos modelos, processa normalmente
        if falta.cod_produto not in produtos_faltantes:
            produtos_faltantes[falta.cod_produto] = {
                'nome_produto': produto.name if produto else 'Produto não encontrado',
                'faltas': []  # Lista para armazenar os detalhes de cada pedido
            }

        # Adiciona os detalhes do pedido à lista de faltas do produto
        produtos_faltantes[falta.cod_produto]['faltas'].append({
            'pedido_id': falta.pedido.id,
            'cliente': falta.pedido.cliente.name,
            'quantidade_pedido': falta.quantidade_pedido,
            'quantidade_separada': falta.quantidade_separada,
            'quantidade_faltante': falta_qtd
        })

    # Renderiza a página HTML com o contexto
    return render(request, 'pedidos/faltas_pedidos.html', {'produtos_faltantes': produtos_faltantes})



def lancar_saida(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        transportadora = request.POST.get("transportadora")
        data_saida = request.POST.get("data_saida")
        valor_frete = request.POST.get("valor_frete")
        observacoes = request.POST.get("observacoes")

        # Salvar no banco de dados
        SaidaPedido.objects.create(
            pedido=pedido,
            transportadora=transportadora,
            data_saida=data_saida,
            valor_frete=valor_frete,
            observacoes=observacoes,
        )

        messages.success(request, "Saída registrada com sucesso!")
        return redirect('listar_pedidos')

    return render(request, 'pedidos/lancar_saida.html', {'pedido': pedido})

