from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TransferenciaEstoqueSaidaInfo, TransferenciaEstoqueSaidaProdutos
from cadastros.models import Products


def entrada_produtos_acabados(request):
    if request.method == 'GET':
        produtos = Products.objects.all()
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
        codigos_barra_unidade = request.POST.getlist('codigo_barra_unidade')
        codigos_barra_caixa = request.POST.getlist('codigo_barra_caixa')


        if TransferenciaEstoqueSaidaProdutos.objects.filter(lote="1234").exists():
            print('lote ja existe')

        try:

            for i in range(len(produtos_inputs)):
                produto = Products.objects.get(name=produtos_inputs[i])
                quantidade_unitaria = quantidades_unitarias[i]
                quantidade_caixa = quantidades_caixas[i]
                lote = lotes[i]
                data_fabricacao = datas_fabricacao[i]
                validade = validades[i]

                if not produto:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Produto não informado'})
                elif not quantidade_unitaria:
                    print('erro quantidade')
                    return render(request, 'produtos_acabados/erro.html',
                                  {'error': 'Quantidade Unitaria nao informada'})
                elif not quantidade_caixa:
                    return render(request, 'produtos_acabados/erro.html',
                                  {'error': 'Quantidade de caixas não informada'})

                elif not lote or TransferenciaEstoqueSaidaProdutos.objects.filter(lote=lote).exists():
                    return render(request, 'produtos_acabados/erro.html',
                                  {'error': 'Lote nao informado ou ja existente'})

                elif not data_fabricacao:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Data de fabricação não informada'})
                elif not validade:
                    return render(request, 'produtos_acabados/erro.html', {'error': 'Data de validade não informada'})

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
                    )
                    # Associando o produto à transferência de estoque de saída
                    transferencia_info.transferenciaestoquesaidaprodutos_set.add(transferencia_produto)

                return redirect('entrada_produtos_acabados')  # Redireciona para alguma outra view após o processamento

        except Exception as e:
            return render(request, 'produtos_acabados/erro.html', {'error': str(e)})

    return HttpResponse(status=405)  # Método não permitido


def listar_transferencias_estoque(request):
    transferencias = TransferenciaEstoqueSaidaInfo.objects.all()
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html',
                  {'transferencias': transferencias, 'opcao': 'saida'})



def listar_transferecias_para_conferencia(request):
    transferencias = TransferenciaEstoqueSaidaInfo.objects.all()
    return render(request, 'produtos_acabados/listar_transferencias_estoque.html',
                  {'transferencias': transferencias, 'opcao': 'entrada'})



def exibir_transferencias_estoque(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=id)
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)
        return render(request, 'produtos_acabados/exibir_transferencias_estoque.html', {'transferencia': transferencia,
                                                                                        'produtos': produtos})


def receber_transferencia_estoque(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        transferencia = TransferenciaEstoqueSaidaInfo.objects.get(numero_transferencia=id)
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(numero_transferencia=transferencia)
        return render(request, 'produtos_acabados/receber_transferencia_estoque.html', {'transferencia': transferencia,
                                                                                        'produtos': produtos})

