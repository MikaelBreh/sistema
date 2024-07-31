from django.core.exceptions import ObjectDoesNotExist

from cadastros.models import Products
from produtos_acabados.models import TransferenciaEstoqueSaidaProdutos


def product_bar_code_is_valid(codigo_barra, nome_produto):

    try:
        produto = Products.objects.get(product_bar_code=codigo_barra)

        if produto.name == nome_produto:
            return True

        else:
            return False

    except ObjectDoesNotExist:
        return None


def box_bar_code_is_valid(codigo_barra_caixa, nome_produto):

    try:
        produto = Products.objects.get(box_bar_code=codigo_barra_caixa)

        if produto.name == nome_produto:
            return True

        else:
            return False

    except ObjectDoesNotExist:
        return None


def verificar_duplicidade_lote(lote_input, nome_produto):
    try:
        produtos = TransferenciaEstoqueSaidaProdutos.objects.filter(lote=lote_input)

        for produto in produtos:
            if str(produto.produto.name) != str(nome_produto):
                return False

    except Exception as e:
        print(f'Erro ao verificar duplicidade: {str(e)}')
        return False
