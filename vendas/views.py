from itertools import chain

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cadastros.models import Clientes, Products, TabelaPrecoProduto, Products_another_info

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Exists, OuterRef

from .functions.validar_separacao import validar_lote
from .models import Pedido, PedidoItem, PedidoSeparacao

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
def criar_pedido_separacao(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Clientes, id=cliente_id)

        pedido = Pedido.objects.create(cliente=cliente)

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

        return render(request, 'vendas/criar_pedido_separacao.html',
                      {'clientes': nomes_clientes_all, 'produtos': nome_produtos_all})


@login_required
def visualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    itens_pedido = PedidoItem.objects.filter(pedido=pedido)

    # Carregar os objetos relacionados
    for item in itens_pedido:
        content_type = ContentType.objects.get_for_id(item.content_type_id)
        model_class = content_type.model_class()
        item.product_instance = model_class.objects.get(id=item.object_id)

    return render(request, 'vendas/visualizar_pedido.html', {'pedido': pedido, 'itens_pedido': itens_pedido})


@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Clientes, id=cliente_id)
        pedido.cliente = cliente
        pedido.save()

        PedidoItem.objects.filter(pedido=pedido).delete()

        produtos = request.POST.getlist('nome_produto')
        quantidades = request.POST.getlist('quantidade_produto')
        quantidades_caixas = request.POST.getlist('quantidade_caixas')

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
                return HttpResponse("Erro ao atualizar pedido")

        return redirect('listar_pedidos')

    else:
        nomes_clientes_all = Clientes.objects.all()
        nome_produtos_all = list(chain(Products.objects.all(), Products_another_info.objects.all()))
        itens_pedido = PedidoItem.objects.filter(pedido=pedido)

        for item in itens_pedido:
            content_type = ContentType.objects.get_for_id(item.content_type_id)
            model_class = content_type.model_class()
            item.product_instance = model_class.objects.get(id=item.object_id)

        return render(request, 'vendas/editar_pedido.html',
                      {'pedido': pedido, 'clientes': nomes_clientes_all, 'produtos': nome_produtos_all, 'itens_pedido': itens_pedido})


@login_required
@csrf_exempt
def aprovar_pedido(request, pedido_id):
    if request.method == 'POST':
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.aprovado = True
            pedido.save()
            return JsonResponse({'success': True})
        except Pedido.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido não encontrado.'})
    return JsonResponse({'success': False, 'error': 'Método não permitido.'})


@login_required
def listar_pedidos_por_status(request, status):
    # Filtra os pedidos com base no status passado como argumento
    pedidos = Pedido.objects.filter(status=status).order_by('-data')

    # Serializa os dados dos pedidos para JSON
    data = [{
        'numero_pedido': pedido.id,  # Usando o id como número do pedido
        'cliente': pedido.cliente.name,
        'data': pedido.data.strftime('%d/%m/%Y'),
        'status': pedido.get_status_display(),
    } for pedido in pedidos]

    # Retorna a lista de pedidos como uma resposta JSON
    return JsonResponse({'pedidos': data})



def listar_pedidos(request):
    return render(request, 'pedidos/lista_pedidos.html')  # Renderiza o template HTML



def alterar_status_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        novo_status = request.POST.get('novo_status')

        if novo_status:
            pedido.status = novo_status
            pedido.save()
            return redirect('listar_pedidos_por_status',
                            status=novo_status)  # Redireciona para a listagem com o novo status
        else:
            return HttpResponse("Status inválido", status=400)



# EXPEDICAO -- AQUI COMECA A PARTE DA SEPARACAO DE PEDIDOS


@login_required
def expedicao_list(request):
    search_query = request.GET.get('search', '')

    # Subquery para verificar se o pedido tem separação
    separacoes_existem = PedidoSeparacao.objects.filter(pedido=OuterRef('pk'))

    if search_query:
        pedidos = Pedido.objects.filter(
            Q(cliente__name__icontains=search_query) &
            Q(aprovado=True) &
            ~Exists(separacoes_existem)  # Filtro para pedidos sem separação
        )
    else:
        pedidos = Pedido.objects.filter(
            Q(aprovado=True) &
            ~Exists(separacoes_existem)  # Filtro para pedidos sem separação
        )

    paginator = Paginator(pedidos, 10)  # Mostra 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendas/expedicao_list.html', {'pedidos': page_obj})


@login_required
def expedicao_separando_list_view(request):
    search_query = request.GET.get('search', '')

    # Subquery para verificar se o pedido tem separação
    separacoes_existem = PedidoSeparacao.objects.filter(pedido=OuterRef('pk'))

    if search_query:
        pedidos = Pedido.objects.filter(
            Q(cliente__name__icontains=search_query) &
            Q(aprovado=True) &
            Q(finalizado=False) &  # Adiciona filtro para 'finalizado' ser falso
            Exists(separacoes_existem)
        )
    else:
        pedidos = Pedido.objects.filter(
            Q(aprovado=True) &
            Q(finalizado=False) &  # Adiciona filtro para 'finalizado' ser falso
            Exists(separacoes_existem)
        )

    paginator = Paginator(pedidos, 10)  # Mostra 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendas/expedicao_list.html', {'pedidos': page_obj, 'separando': True})


@login_required
def expedicao_separar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        try:
            for item in pedido.itens.all():
                lotes = request.POST.getlist(f'lotes_{item.id}')
                quantidades = request.POST.getlist(f'quantidades_{item.id}')
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
                            return render(request, 'vendas/expedicao_separar.html', {'pedido': pedido})

                        # Acumula a quantidade separada
                        quantidade_int = int(quantidade)
                        total_quantidade += quantidade_int

                        if total_quantidade > item.quantidade:
                            raise ValidationError(
                                f"A quantidade separada para {item.produto.name} excede a quantidade do pedido."
                            )

                        # Cria o registro na tabela PedidoSeparacao
                        PedidoSeparacao.objects.create(
                            pedido=pedido,
                            item_pedido=item,
                            lote=lote,
                            quantidade=quantidade_int
                        )

            messages.success(request, "Pedido salvo com sucesso!")
            # Se tudo der certo, salvar e mostar novamente a tela de separacao
            return redirect('expedicao_separar_editar', pedido_id=pedido_id)

        except ValidationError as e:
            # Captura a exceção de validação e adiciona uma mensagem de erro
            messages.error(request, str(e))

    # Recarrega a página com a mensagem de erro (se houver)
    return render(request, 'vendas/expedicao_separar.html', {'pedido': pedido})


@login_required
def expedicao_ver(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'vendas/expedicao_ver.html', {'pedido': pedido})


@login_required
def expedicao_ver_separacao(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido)

    return render(request, 'vendas/expedicao_ver_separacao.html', {
        'pedido': pedido,
        'separacoes': separacoes
    })


@login_required
def expedicao_separar_editar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    separacoes = PedidoSeparacao.objects.filter(pedido=pedido).select_related('item_pedido')

    if request.method == 'POST':
        try:
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

            # Adiciona mensagem de sucesso e redireciona
            messages.success(request, 'Separação do pedido atualizada com sucesso.')
            return redirect('expedicao_separar_editar', pedido_id=pedido_id)

        except ValidationError as e:
            # Captura a exceção de validação e adiciona uma mensagem de erro
            messages.error(request, str(e))

    return render(request, 'vendas/expedicao_separar_editar.html', {
        'pedido': pedido,
        'separacoes': separacoes,
    })











