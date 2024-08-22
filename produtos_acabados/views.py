from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django import forms

from .models import TransferenciaEstoqueSaidaInfo, TransferenciaEstoqueSaidaProdutos, MistoItem, MistoComponent
from cadastros.models import Products, Products_another_info
from .view_functions.get_produtos import product_bar_code_is_valid, box_bar_code_is_valid, verificar_duplicidade_lote


@login_required
def entrada_produtos_acabados(request):
    if request.method == 'GET':
        produtos = Products.objects.filter(category='fabricado')
        return render(request, 'produtos_acabados/entrada_produtos_acabados.html', {'produtos': produtos})

    elif request.method == 'POST':
        # Capturando dados do formulário
        motorista = request.POST.get('motorista_input')
        veiculo = request.POST.get('veiculo_input')
        conferente = request.POST.get('conferente_input')
        quantidade_pallets = request.POST.get('quantidade_pallets')
        observacoes = request.POST.get('obs_input')
        produtos_inputs = request.POST.getlist('produto_input')
        quantidades_unitarias = request.POST.getlist('quantidade_produto')
        quantidades_caixas = request.POST.getlist('quantidade_caixas_produto')
        lotes = request.POST.getlist('lote_produto')
        datas_fabricacao = request.POST.getlist('data_fabricacao_produto')
        validades = request.POST.getlist('data_validade_produto')
        codigos_barra_unidade = request.POST.getlist('codigo_barras_produto')
        codigos_barra_caixa = request.POST.getlist('codigo_barras_caixa_produto')


        try:

            for i in range(len(produtos_inputs)):
                produto = Products.objects.get(name=produtos_inputs[i])
                quantidade_unitaria = quantidades_unitarias[i]
                quantidade_caixa = quantidades_caixas[i]
                lote = lotes[i]
                data_fabricacao = datas_fabricacao[i]
                validade = validades[i]
                correto_codigos_barra_unidade = codigos_barra_unidade[i]
                correto_codigos_barra_caixa = codigos_barra_caixa[i]

                if not produto:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Produto não informado'})
                elif not quantidade_unitaria:
                    print('erro quantidade')
                    return render(request, 'produtos_acabados/erro.html',
                                  {'error': 'Quantidade Unitaria nao informada'})
                elif not quantidade_caixa:
                    return render(request, 'produtos_acabados/erro.html',
                                  {'error': 'Quantidade de caixas não informada'})

                elif not lote:
                    return render(request, 'produtos_acabados/erro.html',
                                  {'error': 'Lote nao informado'})

                elif verificar_duplicidade_lote(lote, produto) is False:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Lote já cadastrado | Produto: ' +
                                                                                    produto.name + ' | Lote: ' + lote})

                elif not data_fabricacao:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Data de fabricação não informada'})
                elif not validade:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Data de validade não informada'})

                elif not correto_codigos_barra_unidade or not correto_codigos_barra_caixa:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Código de barras ou de caixa não '
                                                                                    'informado'})

                elif product_bar_code_is_valid(correto_codigos_barra_unidade, produto) is None or False:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Codigo de barras incorreto ou '
                                                                                    'diferente do produto selecionado'})

                elif box_bar_code_is_valid(correto_codigos_barra_caixa, produto) is None or False:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Codigo de barras da caixa '
                                                                                    'incorreto ou '
                                                                                    'diferente do produto selecionado'})



            for i in range(len(produtos_inputs)):

                # Criando instancia de transferencia_estoque_saida_info
                transferencia_info = TransferenciaEstoqueSaidaInfo.objects.create(
                    motorista=motorista,
                    veiculo=veiculo,
                    conferente=conferente,
                    quantidade_pallets=quantidade_pallets,
                    observacoes=observacoes,
                )

                # Criando instancias de transferencia_estoque_saida_produtos e associando com a transferência
                for j in range(len(produtos_inputs)):
                    produto = Products.objects.get(name=produtos_inputs[j])
                    transferencia_produto = TransferenciaEstoqueSaidaProdutos.objects.create(
                        numero_transferencia=transferencia_info,  # Associando à transferência criada
                        produto=produto,
                        quantidade_unitaria=quantidades_unitarias[j],
                        quantidade_caixa=quantidades_caixas[j],
                        lote=lotes[j],
                        data_fabricacao=datas_fabricacao[j],
                        validade=validades[j],
                        codigo_barra_unidade=codigos_barra_unidade[j],
                        codigo_barra_caixa=codigos_barra_caixa[j]
                    )
                    # Associando o produto à transferência de estoque de saída
                    transferencia_info.transferenciaestoquesaidaprodutos_set.add(transferencia_produto)

                return redirect('listar_transferencias_estoque')  # Redireciona para alguma outra view após o processamento

        except Exception as e:
            return render(request, 'produtos_acabados/erro.html', {'error': str(e)})

    return HttpResponse(status=405)  # Método não permitido


@login_required
def listar_transferencias_estoque(request):
    transferencias = TransferenciaEstoqueSaidaInfo.objects.filter(validado=False)
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html',
                  {'transferencias': transferencias, 'opcao': 'saida'})


@login_required
def listar_transferecias_para_conferencia(request):
    transferencias = TransferenciaEstoqueSaidaInfo.objects.filter(validado=False)
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html',
                  {'transferencias': transferencias, 'opcao': 'entrada'})


@login_required
def exibir_transferencias_estoque(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=id)
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)
        return render(request, 'produtos_acabados/exibir_transferencias_estoque.html', {'transferencia': transferencia,
                                                                                        'produtos': produtos})


@login_required
def receber_transferencia_estoque(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=id)
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)
        return render(request, 'produtos_acabados/receber_transferencia_estoque.html', {'transferencia': transferencia,
                                                                                        'produtos': produtos})

    if request.method == 'POST':
        pk = request.GET.get('id')
        transferencia = get_object_or_404(TransferenciaEstoqueSaidaInfo, pk=pk)

        transferencia.validado = True
        transferencia.save()
        return redirect('entradas_recebidas_estoque')


@login_required
def listar_transferencias_recebidas(request):
    transferencias = TransferenciaEstoqueSaidaInfo.objects.filter(validado=True)
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html',
                  {'transferencias': transferencias, 'opcao': 'recebida'})


@login_required
def lista_produtos_estoque(request):
    query = request.GET.get('q')
    produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(
        numero_transferencia__validado=True
    )

    if query:
        produtos = produtos.filter(
            Q(produto__name__icontains=query) |
            Q(lote__icontains=query) |
            Q(codigo_barra_unidade__icontains=query)
        )

    paginator = Paginator(produtos, 10)  # 10 produtos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'produtos_acabados/lista_produtos_estoque.html', {'page_obj': page_obj, 'query': query})


@login_required
def create_misto_item(request):
    if request.method == 'GET':
        produtos_principal = Products.objects.filter(category='misto')
        produtos_misto_another_info = Products_another_info.objects.filter(produto_pertence__category='misto')


        produtos_geral = Products.objects.filter(category='fabricado')
        produtos_outra_info = Products_another_info.objects.filter(produto_pertence__category='fabricado')


        # Criar uma lista combinada
        produtos_combinados = list(produtos_principal) + list(produtos_misto_another_info)

        # criar uma lista combinada de todos os produtos

        produtos_geral_combinados = list(produtos_geral) + list(produtos_outra_info)

        return render(request, 'produtos_acabados/itens_mistos/create_item_misto.html',
                      {'produtos': produtos_combinados, 'produtos_geral': produtos_geral_combinados})



    if request.method == 'POST':
        produto_input = request.POST.get('produto_input')
        lote = request.POST.get('lote')
        quantidade_unitaria = request.POST.get('quantidade_unitaria')

        if not produto_input:
            return render(request, 'produtos_acabados/erro.html', {'error': 'Produto Misto não informado'})
        elif not lote:
            return render(request, 'produtos_acabados/erro.html', {'error': 'Lote não informado'})
        elif not quantidade_unitaria:
            return render(request, 'produtos_acabados/erro.html', {'error': 'Quantidade unitária não informada'})

        # Tentar encontrar o produto no modelo Products
        try:
            produto = Products.objects.get(name=produto_input)
        except Products.DoesNotExist:
            try:
                produto = Products_another_info.objects.get(name=produto_input).produto_pertence
            except Products_another_info.DoesNotExist:
                return render(request, 'produtos_acabados/erro.html', {'error': 'Produto não encontrado'})

        # Criar o MistoItem
        misto_item = MistoItem.objects.create(
            content_type=ContentType.objects.get_for_model(Products),
            object_id=produto.pk,
            produto_nome=produto_input,
            lote=lote,
            quantidade_unitaria=int(quantidade_unitaria)
        )

        # Coletar e salvar os componentes
        componentes = []
        produtos_componentes = request.POST.getlist('produto_component')
        lotes_componentes = request.POST.getlist('lote_component')
        quantidades_caixa_componentes = request.POST.getlist('quantidade_caixa_component')

        for idx in range(len(produtos_componentes)):
            produto_component = produtos_componentes[idx]
            lote_component = lotes_componentes[idx]
            quantidade_caixa_component = quantidades_caixa_componentes[idx]

            if produto_component and lote_component and quantidade_caixa_component:
                try:
                    produto_geral = Products.objects.get(name=produto_component)
                except Products.DoesNotExist:
                    try:
                        produto_geral = Products_another_info.objects.get(name=produto_component).produto_pertence
                    except Products_another_info.DoesNotExist:
                        continue

                componente = MistoComponent(
                    misto_item=misto_item,
                    content_type=ContentType.objects.get_for_model(Products),
                    object_id=produto_geral.pk,
                    produto=produto_geral,
                    lote=lote_component,
                    quantidade=int(quantidade_caixa_component)
                )
                componentes.append(componente)

        # Salvar todos os componentes de uma vez
        if componentes:
            MistoComponent.objects.bulk_create(componentes)

        return redirect('list_misto_item')  # Redirecionar para uma página de sucesso ou outra página desejada

    return render(request, 'produtos_acabados/criar_item_misto.html')


@login_required
def list_item_misto(request):
    misto_items = MistoItem.objects.all()

    return render(request, 'produtos_acabados/itens_mistos/list_item_misto.html',
                  {'misto_items': misto_items})


@login_required
def visualizar_misto_item(request, misto_pk):
    misto_item = MistoItem.objects.get(pk=misto_pk)
    componentes = MistoComponent.objects.filter(misto_item=misto_item)

    return render(request, 'produtos_acabados/itens_mistos/visualizar_misto_item.html',
                  {'misto_item': misto_item, 'componentes': componentes})









