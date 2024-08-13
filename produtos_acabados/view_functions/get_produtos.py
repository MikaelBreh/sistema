from django.core.exceptions import ObjectDoesNotExist

from cadastros.models import Products
from produtos_acabados.models import TransferenciaEstoqueSaidaProdutos


def product_bar_code_is_valid(codigo_barra, nome_produto):
    produtos = Products.objects.filter(product_bar_code=codigo_barra)

    if produtos.exists():
        for produto in produtos:
            if produto.name == nome_produto:
                return True
        return False  # Nenhum dos produtos com o código de barra tem o nome esperado
    else:
        return None  # Não foi encontrado nenhum produto com esse código de barra


def box_bar_code_is_valid(codigo_barra_caixa, nome_produto):
    produtos = Products.objects.filter(box_bar_code=codigo_barra_caixa)

    if produtos.exists():
        for produto in produtos:
            if produto.name == nome_produto:
                return True
        return False  # Nenhum dos produtos com o código de barra tem o nome esperado
    else:
        return None  # Não foi encontrado nenhum produto com esse código de barra


def verificar_duplicidade_lote(lote_input, nome_produto):
    try:
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(lote=lote_input)

        for produto in produtos:
            if str(produto.produto.name) != str(nome_produto):
                return False

    except Exception as e:
        print(f'Erro ao verificar duplicidade: {str(e)}')
        return False
