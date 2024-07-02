from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Products, Clientes, Vendedores
from cadastros.cadastro_logica.estatico_dicionario_banco_titulos.dict_produtos_exibicao_em_lista import \
    dicionario_produtos, dicionario_clientes, dicionario_vendedeores


# Create your views here.
def exbicao_cadastros_produtos_lista(request, modulo):

    if modulo == 'Produtos':
        produtos = Products.objects.all()

        return render(request, 'cadastros/exibicao_cadastros.html', {'valores': produtos, 'modulo': modulo,
                                                                     'dicionario': dicionario_produtos})



    elif modulo == 'Clientes':
        clientes = Clientes.objects.all()
        return render(request, 'cadastros/exibicao_cadastros.html', {'valores': clientes, 'modulo': modulo,
                                                                     'dicionario': dicionario_clientes})

    # elif modulo == 'Materiais de Trabalho':
    #     materiais_de_trabalho = Materiais_de_Trabalho.objects.all()
    #     return render(request, 'cadastros/exibicao_cadastros.html', {'valores': materiais_de_trabalho, 'modulo': modulo,
    #                                                                  'dicionario': dicionario_materiais_de_trabalho})

    # elif modulo == 'Fornecedores':
    #     fornecedores = Fornecedores.objects.all()
    #     return render(request, 'cadastros/exibicao_cadastros.html', {'valores': fornecedores, 'modulo': modulo,
    #                                                                  'dicionario': dicionario_fornecedores})

    elif modulo == 'Vendedores':
        vendedores = Vendedores.objects.all()
        return render(request, 'cadastros/exibicao_cadastros.html', {'valores': vendedores, 'modulo': modulo,
                                                                     'dicionario': dicionario_vendedeores})



# class ProdutoCreate(CreateView):
#     model = Products
#     fields = ['name', 'product_code', 'product_bar_code', 'box_bar_code', 'ncm', 'cest', 'category']
#     template_name = 'cadastros/cadastrar_novo_produto.html'
#     success_url = '/cadastro/'


# class ProdutoUpdate(UpdateView):
#     model = Products
#     fields = ['name', 'product_code', 'product_bar_code', 'box_bar_code', 'ncm', 'cest', 'category']
#     template_name = 'cadastros/cadastrar_novo_produto.html'
#     success_url = '/cadastro/'


# class ProdutoDelete(DeleteView):
#     model = Products
#     template_name = 'cadastros/cadastrar_novo_produto.html'
#     success_url = '/cadastro/'


class CampoList(ListView):
    model = Products
    template_name = 'cadastros/exibicao_cadastros.html'



def exibir_cadastro_produto(request):

    if request.method == 'GET':
        id = request.GET.get('id')
        product = Products.objects.get(id=id)
        return render(request, 'cadastros/exibir_cadastro_produto.html', {'produto': product})

    return render(request, 'cadastros/exibir_cadastro_produto.html')




