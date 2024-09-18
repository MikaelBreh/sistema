from django.shortcuts import render, get_object_or_404
from cadastros.models import Products, Products_another_info
from django.contrib.auth.decorators import login_required

from cadastros.models import Products, Products_another_info
from produtos_acabados.models import TransferenciaEstoqueSaidaProdutos, MistoItem
from vendas.models import Pedido, PedidoSeparacao


@login_required
def visualizar_estoque(request):

    if request.method == 'GET':

        # Consulta para trazer todos os produtos e produtos_another_info
        produtos = Products.objects.all()
        produtos_another_info = Products_another_info.objects.all()

        # -------------------------------------------------------


        # Consulta para filtrar os produtos e quantidades unitárias onde o a transferencia é validada
        entrada_produtos_validados = TransferenciaEstoqueSaidaProdutos.objects.filter(
            numero_transferencia__validado=True).values('produto__name', 'quantidade_unitaria')

        dicionario_entrada_produtos = {}
        for produto in entrada_produtos_validados:

            if produto['produto__name'] in dicionario_entrada_produtos:
                dicionario_entrada_produtos[produto['produto__name']] += produto['quantidade_unitaria']

            else:
                dicionario_entrada_produtos[produto['produto__name']] = produto['quantidade_unitaria']

        # print(dicionario_entrada_produtos)

        # -------------------------------------------------------

        # Consulta para obter o produto e a quantidade unitaria do item misto criado
        misto_items = MistoItem.objects.all()

        # Exibir os resultados com o nome do produto em vez do objeto
        dicionario_mistos_criados = {}
        for item in misto_items:

            if item.produto_misto.name in dicionario_mistos_criados:
                dicionario_mistos_criados[item.produto_misto.name] += item.quantidade_unitaria

            else:
                dicionario_mistos_criados[item.produto_misto.name] = item.quantidade_unitaria

        # print(dicionario_mistos_criados)

        # -------------------------------------------------------

        dicionario_mistos_componentes = {}
        # Consulta para obter o produto, quantidade e quantidade de caixas dos componentes de misto_items
        for misto_item in misto_items:
            quantidade_de_caixas = misto_item.quantidade_de_caixas
            components = misto_item.components.all()

            for component in components:
                produto = component.produto
                quantidade = component.quantidade

                if produto.name in dicionario_mistos_componentes:
                    dicionario_mistos_componentes[produto.name] += quantidade * quantidade_de_caixas
                else:
                    dicionario_mistos_componentes[produto.name] = quantidade * quantidade_de_caixas

        # print(dicionario_mistos_componentes)

        # -------------------------------------------------------

        pedidos = Pedido.objects.all()

        # -------------------------------------------------------

        dicionario_produtos_pedidos_finalizados = {}
        # Pegar dads Pedidos
        for pedido in pedidos:
            status_pedido = pedido.status

            pedido_itens = pedido.itens.all()

            for item in pedido_itens:
                componente = item.produto
                quantidade = item.quantidade

                if status_pedido == 12:
                    if componente.name in dicionario_produtos_pedidos_finalizados:
                        dicionario_produtos_pedidos_finalizados[componente.name] += quantidade
                    else:
                        dicionario_produtos_pedidos_finalizados[componente.name] = quantidade

        # print(dicionario_produtos_pedidos_finalizados)

        # -------------------------------------------------------

        dicionario_produtos_pedidos_separados = {}
        # pegar produtos que ja estao separados

        produtos_separados = PedidoSeparacao.objects.all()

        for produto_separado in produtos_separados:
            produto = produto_separado.item_pedido.produto
            quantidade = produto_separado.quantidade

            if produto.name in dicionario_produtos_pedidos_separados:
                dicionario_produtos_pedidos_separados[produto.name] += quantidade
            else:
                dicionario_produtos_pedidos_separados[produto.name] = quantidade

        for produto_another in produtos_another_info:
            produto_base_name = produto_another.produto_pertence.name
            produto_another_name = produto_another.name  # Nome do produto no Products_another_info

            # Verifica se o produto_another está no dicionário usando o nome do produto
            if produto_another_name in dicionario_produtos_pedidos_separados:
                # Se já existe uma entrada para o produto base, soma a quantidade
                if produto_base_name in dicionario_produtos_pedidos_separados:
                    dicionario_produtos_pedidos_separados[
                        produto_base_name] += dicionario_produtos_pedidos_separados.pop(produto_another_name)
                else:
                    # Caso contrário, apenas mova o valor de produto_another para produto_base_name
                    dicionario_produtos_pedidos_separados[
                        produto_base_name] = dicionario_produtos_pedidos_separados.pop(produto_another_name)


        print(dicionario_produtos_pedidos_separados)





        # -------------------------------------------------------

        # Corrigindo dicionario de entrada de produtos
        for produto in produtos:
            try:
                tentativa = dicionario_entrada_produtos[produto.name]

            except KeyError:
                dicionario_entrada_produtos[produto.name] = 0

        # print(dicionario_entrada_produtos)

        # -------------------------------------------------------
        # Corrigindo dicionario de componentes usados nos mistos
        for produto in produtos:
            try:
                tentativa = dicionario_mistos_componentes[produto.name]

            except KeyError:
                dicionario_mistos_componentes[produto.name] = 0

        # print(dicionario_mistos_componentes)
        # -------------------------------------------------------

        # Corrigindo dicionario de mistos criados
        # Preenchendo o dicionário com os produtos principais
        for produto in produtos:
            try:
                tentativa = dicionario_mistos_criados[produto.name]
            except KeyError:
                dicionario_mistos_criados[produto.name] = 0

        # print(dicionario_mistos_criados)
        # -------------------------------------------------------

        # Aqui pegamos os produtos que sairam nos pedidos que estao finalizados, (status == 12) e somamos a quantidade
        # incluindo os produtos que sao diferentes (products_another_info) e associamos ao produto base

        dicionario_produtos_finalizados_corrigido = {}

        # Corrigindo dicionário de produtos finalizados, associando produtos_another_info aos produtos base
        for produto_another in produtos_another_info:
            produto_base_name = produto_another.produto_pertence.name
            if produto_base_name in dicionario_produtos_finalizados_corrigido:
                dicionario_produtos_finalizados_corrigido[
                    produto_base_name] += dicionario_produtos_pedidos_finalizados.get(produto_another.name, 0)
            else:
                dicionario_produtos_finalizados_corrigido[
                    produto_base_name] = dicionario_produtos_pedidos_finalizados.get(produto_another.name, 0)

        # Preenchendo o dicionário com os produtos principais
        for produto in produtos:
            produto_name = produto.name
            if produto_name in dicionario_produtos_finalizados_corrigido:
                dicionario_produtos_finalizados_corrigido[produto_name] += dicionario_produtos_pedidos_finalizados.get(
                    produto_name, 0)
            else:
                dicionario_produtos_finalizados_corrigido[produto_name] = dicionario_produtos_pedidos_finalizados.get(
                    produto_name, 0)

        # print(dicionario_produtos_finalizados_corrigido)

        # -------------------------------------------------------

        # agora vamos criar um unico dicionario com os produtos e quantidades em estoque

        lista_produtos = []
        lista_quantidades = []
        lista_quantidade_separadas= []

        for produto in produtos:
            produto_name = produto.name

            quantidade_entrada = dicionario_entrada_produtos[produto_name]
            quantidade_mistos = dicionario_mistos_criados[produto_name]
            quantidade_componentes = dicionario_mistos_componentes[produto_name]
            quantidade_finalizados = dicionario_produtos_finalizados_corrigido[produto_name]

            try:
                quantidade_separados = dicionario_produtos_pedidos_separados[produto_name]
            except KeyError:
                quantidade_separados = 0

            quantidade_total = (quantidade_entrada + quantidade_mistos) - (quantidade_componentes + quantidade_finalizados + quantidade_separados)

            lista_produtos.append(produto_name)
            lista_quantidades.append(quantidade_total)
            lista_quantidade_separadas.append(quantidade_separados)


        # Criando a lista de pares (produto, quantidade)
        produtos_quantidades = zip(lista_produtos, lista_quantidades, lista_quantidade_separadas)

        return render(request, 'estoque/visualizar_estoque.html',
                      {'produtos_quantidades': produtos_quantidades,})











