from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime

from estoque.models import Estoque
from .models import TransferenciaEstoqueSaidaInfo, TransferenciaEstoqueSaidaProdutos, MistoItem, MistoComponent
from cadastros.models import Products, Products_another_info



# Aqui criamos a transferencia de estoque (motorista, etc)
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

        try:

            # Criando instancia de transferencia_estoque_saida_info
            transferencia_info = TransferenciaEstoqueSaidaInfo.objects.create(
                motorista=motorista,
                veiculo=veiculo,
                conferente=conferente,
                quantidade_pallets=quantidade_pallets,
                observacoes=observacoes,
            )

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
def exibir_transferencias_estoque(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=id)
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)

        status = ''
        if not transferencia.validado:
            status = 'n_validado'

        return render(request, 'produtos_acabados/exibir_transferencias_estoque.html', {'transferencia': transferencia,
                                                                                        'produtos': produtos, 'id': id,
                                                                                        'status': status})


def adicionar_produto_transferencia(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        produtos = Products.objects.all()
        return render(request, 'produtos_acabados/adicionar_produto_transferencia.html',
                      {'id': id, 'produtos': produtos})

    if request.method == 'POST':
        # Capturando a transferência (id)
        transferencia_id = request.GET.get('id')

        # Capturando a transferência do banco de dados
        try:
            transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=transferencia_id)
        except TransferenciaEstoqueSaidaInfo.DoesNotExist:
            return render(request, 'produtos_acabados/erro.html', {'error': 'Transferência não encontrada'})

        # Capturando dados do formulário
        produtos_inputs = request.POST.get('produto_input')
        quantidades_unitarias = request.POST.get('quantidade_produto')
        quantidades_caixas = request.POST.get('quantidade_caixas_produto')
        lotes = request.POST.get('lote_produto')
        datas_fabricacao = request.POST.get('data_fabricacao_produto')
        validades = request.POST.get('data_validade_produto')
        codigos_barra_unidade = request.POST.get('codigo_barras_produto')
        codigos_barra_caixa = request.POST.get('codigo_barras_caixa_produto')

        # Validando se os campos obrigatórios estão presentes
        if not produtos_inputs or not quantidades_unitarias or not quantidades_caixas or not lotes:
            return render(request, 'produtos_acabados/erro.html', {'error': 'Campos obrigatórios não preenchidos'})

        print(produtos_inputs)
        produto_name = produtos_inputs

        try:
            produto = Products.objects.get(name=produto_name)
        except Products.DoesNotExist:
            return render(request, 'produtos_acabados/erro.html',
                          {'error': f'Produto {produto_name} não encontrado'})

        # Validação dos códigos de barras
        codigo_barras_unidade = codigos_barra_unidade
        codigo_barras_caixa = codigos_barra_caixa

        if produto.product_bar_code != codigo_barras_unidade:
            return render(request, 'produtos_acabados/erro.html',
                          {'error': f'Código de barras da unidade incorreto para o produto {produto.name}'})

        if produto.box_bar_code != codigo_barras_caixa:
            return render(request, 'produtos_acabados/erro.html',
                          {'error': f'Código de barras da caixa incorreto para o produto {produto.name}'})

        # Validação do lote
        lote_atual = lotes
        lote_existente = TransferenciaEstoqueSaidaProdutos.objects.filter(lote=lote_atual).first()

        if lote_existente and lote_existente.produto != produto:
            return render(request, 'produtos_acabados/erro.html', {
                'error': f'Lote {lote_atual} já existe para o produto {lote_existente.produto.name}, e não para {produto.name}.'
            })

        # Criando a instância de TransferenciaEstoqueSaidaProdutos
        transferencia_produto = TransferenciaEstoqueSaidaProdutos(
            numero_transferencia=transferencia,
            produto=produto,
            quantidade_unitaria=quantidades_unitarias,
            quantidade_caixa=quantidades_caixas,
            lote=lotes,
            data_fabricacao=datas_fabricacao,
            validade=validades,
            codigo_barra_unidade=codigos_barra_unidade,
            codigo_barra_caixa=codigos_barra_caixa
        )

        # Salvando a instância no banco de dados
        transferencia_produto.save()

        # Redirecionando para a página de exibição da transferência
        return redirect(reverse('exibir_transferencia_estoque') + '?id=' + str(transferencia_id))


@login_required
def listar_transferecias_para_conferencia(request):
    transferencias = TransferenciaEstoqueSaidaInfo.objects.filter(validado=False)
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html',
                  {'transferencias': transferencias, 'opcao': 'entrada'})


@login_required
def receber_transferencia_estoque(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=id)
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)
        return render(request, 'produtos_acabados/receber_transferencia_estoque.html', {
            'transferencia': transferencia,
            'produtos': produtos
        })


    if request.method == 'POST':
        pk = request.GET.get('id')
        transferencia = get_object_or_404(TransferenciaEstoqueSaidaInfo, pk=pk)

        # Validando a transferência
        transferencia.validado = True
        transferencia.save()

        # Adicionando entrada no estoque
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)
        content_type = ContentType.objects.get_for_model(TransferenciaEstoqueSaidaInfo)
        for produto_saida in produtos:
            Estoque.objects.create(
                content_type=content_type,  # Define o tipo do modelo relacionado
                object_id=transferencia.pk,  # ID do objeto relacionado
                cod_produto=produto_saida.produto.product_code,
                lote=produto_saida.lote,
                quantidade=produto_saida.quantidade_unitaria,
                status=True  # Indica que é uma entrada no estoque
            )
        return redirect('entradas_recebidas_estoque')





@login_required
def listar_transferencias_recebidas(request):
    # Busca pelo número da transferência
    query = request.GET.get('q', '')

    # Filtro por intervalo de datas
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Query inicial (transferências validadas, ordenadas por número de transferência)
    transferencias = TransferenciaEstoqueSaidaInfo.objects.filter(validado=True).order_by('-numero_transferencia')

    # Aplicando o filtro de busca
    if query:
        transferencias = transferencias.filter(numero_transferencia__icontains=query)

    # Aplicando o filtro por intervalo de datas
    if data_inicio and data_fim:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d').date()
            transferencias = transferencias.filter(data_saida__range=[data_inicio_dt, data_fim_dt])
        except ValueError:
            # Ignorar erros no formato da data
            pass

    # Paginação com 30 itens por página
    paginator = Paginator(transferencias, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizando a template com os dados
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html', {
        'transferencias': page_obj,
        'opcao': 'recebida',
        'query': query,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    })




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
        produtos_principal = Products.objects.all()
        produtos_misto_another_info = Products_another_info.objects.filter(produto_pertence__category='misto')
        produtos_geral = Products.objects.filter(category='fabricado')
        produtos_outra_info = Products_another_info.objects.filter(produto_pertence__category='fabricado')
        produtos_combinados = list(produtos_principal) + list(produtos_misto_another_info)
        produtos_geral_combinados = list(produtos_geral) + list(produtos_outra_info)

        return render(request, 'produtos_acabados/itens_mistos/create_item_misto.html',
                      {'produtos': produtos_combinados, 'produtos_geral': produtos_geral_combinados})

    if request.method == 'POST':
        # Coletar valores do formulário
        produto_input = request.POST.get('produto_input')
        lote = request.POST.get('lote')
        quantidade_unitaria = request.POST.get('quantidade_unitaria')
        quantidade_caixas = request.POST.get('quantidade_caixas')

        errors = []

        # Verificar se o lote já existe no estoque
        if Estoque.objects.filter(lote=lote).exists():
            errors.append('Lote já existe no estoque.')

        # Validações de campos obrigatórios
        if not produto_input:
            errors.append('Produto Misto não informado.')
        if not lote:
            errors.append('Lote não informado.')
        if not quantidade_unitaria:
            errors.append('Quantidade unitária não informada.')
        if not quantidade_caixas:
            errors.append('Quantidade total de caixas não informada.')

        # Recuperar o produto ou `Products_another_info`
        produto = None
        try:
            produto = Products.objects.get(name=produto_input)
        except Products.DoesNotExist:
            try:
                produto_another_info = Products_another_info.objects.get(name=produto_input)
                produto = produto_another_info.produto_pertence  # Referenciar o produto principal
            except Products_another_info.DoesNotExist:
                errors.append('Produto não encontrado.')

        # Verificar erros antes de prosseguir
        if errors:
            return render(request, 'produtos_acabados/erro.html', {'errors': errors})

        # Criação do item misto
        misto_item = MistoItem.objects.create(
            content_type=ContentType.objects.get_for_model(Products),
            object_id=produto.pk,
            produto_nome=produto_input,
            lote=lote,
            quantidade_unitaria=int(quantidade_unitaria),
            quantidade_de_caixas=int(quantidade_caixas)
        )

        # Gerar entrada de estoque para o produto misto criado
        Estoque.objects.create(
            content_type=ContentType.objects.get_for_model(Products),
            object_id=produto.pk,
            fonte=misto_item,
            cod_produto=produto.product_code,
            lote=lote,
            quantidade=int(quantidade_unitaria),
            status=True  # True indica entrada de estoque
        )

        # Processar componentes e gerar saídas de estoque
        produtos_componentes = request.POST.getlist('produto_component')
        lotes_componentes = request.POST.getlist('lote_component')
        quantidades_caixa_componentes = request.POST.getlist('quantidade_caixa_component')

        componentes = []
        for idx in range(len(produtos_componentes)):
            produto_component = produtos_componentes[idx]
            lote_component = lotes_componentes[idx]
            quantidade_caixa_component = quantidades_caixa_componentes[idx]

            if produto_component and lote_component and quantidade_caixa_component:
                try:
                    produto_geral = Products.objects.get(name=produto_component)
                except Products.DoesNotExist:
                    try:
                        produto_another_info_component = Products_another_info.objects.get(name=produto_component)
                        produto_geral = produto_another_info_component.produto_pertence
                    except Products_another_info.DoesNotExist:
                        errors.append(f'Produto componente "{produto_component}" não encontrado.')
                        continue



                # Criar saída de estoque para o componente
                Estoque.objects.create(
                    content_type=ContentType.objects.get_for_model(Products),
                    object_id=produto_geral.pk,
                    fonte=misto_item,
                    cod_produto=produto_geral.product_code,
                    lote=lote_component,
                    quantidade=-int(quantidade_caixa_component) * int(quantidade_caixas),  # Quantidade negativa indica saída de estoque
                    status=False  # False indica saída de estoque
                )

                # Adicionar componente à lista se todas as validações forem bem-sucedidas
                componente = MistoComponent(
                    misto_item=misto_item,
                    content_type=ContentType.objects.get_for_model(Products),
                    object_id=produto_geral.pk,
                    produto=produto_geral,
                    lote=lote_component,
                    quantidade=int(quantidade_caixa_component)
                )
                componentes.append(componente)

        # Salvar componentes no banco de dados
        MistoComponent.objects.bulk_create(componentes)

        return redirect('list_misto_item')





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
