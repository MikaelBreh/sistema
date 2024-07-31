from itertools import chain

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from cadastros.models import Clientes, Products, TabelaPrecoProduto, Products_another_info

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Pedido, PedidoItem

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def home(request):
    if request.method == 'GET':
        nomes_clientes = Clientes.objects.all()
        return render(request, 'vendas/home.html', {'clientes': nomes_clientes})


def get_produtos_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    tabela_preco = cliente.TabelaPreco
    produtos_tabela = TabelaPrecoProduto.objects.filter(tabela_preco=tabela_preco).select_related('produto')
    produtos_data = [{'id': p.produto.id, 'nome': p.produto.name, 'preco': p.valor_sem_impostos} for p in
                     produtos_tabela]
    print(produtos_data)
    return JsonResponse(produtos_data, safe=False)



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




def visualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    itens_pedido = PedidoItem.objects.filter(pedido=pedido)

    # Carregar os objetos relacionados
    for item in itens_pedido:
        content_type = ContentType.objects.get_for_id(item.content_type_id)
        model_class = content_type.model_class()
        item.product_instance = model_class.objects.get(id=item.object_id)

    return render(request, 'vendas/visualizar_pedido.html', {'pedido': pedido, 'itens_pedido': itens_pedido})


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








