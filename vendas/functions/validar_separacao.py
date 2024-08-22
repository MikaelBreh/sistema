from django.contrib.contenttypes.models import ContentType
from cadastros.models import Products_another_info
from produtos_acabados.models import TransferenciaEstoqueSaidaProdutos, MistoItem

def validar_lote(lote, item_pedido):
    produto_principal = item_pedido.produto

    # Verificar se o produto principal é um item misto
    if produto_principal.category == 'misto':
        # Identificar o ContentType do produto principal
        content_type = ContentType.objects.get_for_model(produto_principal)

        # Verificar se o lote existe em MistoItem para o produto principal
        misto_item = MistoItem.objects.filter(
            content_type=content_type,
            object_id=produto_principal.id,
            lote=lote
        ).first()

        if misto_item:
            return misto_item

        # Verificar se o lote pertence a algum Products_another_info relacionado ao produto principal
        produtos_alternativos = Products_another_info.objects.filter(produto_pertence=produto_principal)

        for produto_alternativo in produtos_alternativos:
            # Aqui, pegamos a categoria do produto principal associado
            categoria_produto = produto_alternativo.produto_pertence.category
            content_type_alt = ContentType.objects.get_for_model(produto_alternativo)
            misto_item = MistoItem.objects.filter(
                content_type=content_type_alt,
                object_id=produto_alternativo.id,
                lote=lote
            ).first()
            if misto_item:
                return misto_item

        raise ValueError(f"Lote {lote} não encontrado nos itens mistos do produto {produto_principal} ou em seus produtos alternativos.")

    # Validação original para outros tipos de produto
    lote_produto = TransferenciaEstoqueSaidaProdutos.objects.filter(
        produto=produto_principal,
        lote=lote
    ).first()

    if lote_produto:
        return lote_produto

    # Verificar se o lote pertence a algum Products_another_info relacionado ao produto principal
    produtos_alternativos = Products_another_info.objects.filter(produto_pertence=produto_principal)

    for produto_alternativo in produtos_alternativos:
        # Aqui, pegamos a categoria do produto principal associado
        categoria_produto = produto_alternativo.produto_pertence.category
        lote_produto = TransferenciaEstoqueSaidaProdutos.objects.filter(
            produto=produto_alternativo,
            lote=lote
        ).first()
        if lote_produto:
            return lote_produto

    raise ValueError(f"Lote {lote} não encontrado para o produto {produto_principal} ou em seus produtos alternativos.")
