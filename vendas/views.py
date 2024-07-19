from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from cadastros.models import Clientes, Products, TabelaPrecoProduto


# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def home(request):
    if request.method == 'GET':
        nomes_clientes = Clientes.objects.all()
        return render(request, 'vendas/home.html', {'clientes': nomes_clientes})

def get_produtos_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)
    tabela_preco = cliente.TabelaPreco
    produtos_tabela = TabelaPrecoProduto.objects.filter(tabela_preco=tabela_preco).select_related('produto')
    produtos_data = [{'id': p.produto.id, 'nome': p.produto.name, 'preco': p.valor_sem_impostos} for p in produtos_tabela]
    print(produtos_data)
    return JsonResponse(produtos_data, safe=False)


