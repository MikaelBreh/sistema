import locale

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.shortcuts import render
from django.utils.timezone import now
from datetime import datetime

from cadastros.models import Products
from vendas.models import Pedido, PedidoItem, SaidaPedido, PedidoSeparacao


@login_required
@permission_required('Pedido.view_pedido', raise_exception=True)
def index(request):
    # Data atual e intervalo do mês

    # Configurar o locale para português
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    hoje = now()
    inicio_mes = datetime(hoje.year, hoje.month, 1)
    fim_mes = datetime(hoje.year, hoje.month + 1, 1) if hoje.month < 12 else datetime(hoje.year + 1, 1, 1)

    esse_mes = hoje.strftime('%B')

    # Filtra as saídas no mês atual
    saidas_no_mes = SaidaPedido.objects.filter(
        data_saida__gte=inicio_mes,
        data_saida__lt=fim_mes
    )

    # Obtém os pedidos associados às saídas no mês atual e com status 'finalizados'
    pedidos_finalizados = Pedido.objects.filter(
        id__in=saidas_no_mes.values('pedido_id'),  # Filtra pelo ID dos pedidos na tabela SaidaPedido
        status__iexact='finalizados',             # Status ignorando maiúsculas/minúsculas
    ).count()

    # Filtra a quantidade total de pedidos recebidos esse mes
    quantidade_pedidos_total = Pedido.objects.filter(
        data__gte=inicio_mes,
        data__lt=fim_mes
    ).count()

    # filtra a quantidade de pedidos separados
    quantidade_pedidos_prontos = Pedido.objects.filter(
        status__iexact='separacao_finalizada' or 'conf_separacao'
    ).count()

    # Filtra a quantidade de pedidos em separacao
    quantidade_pedidos_separacao = Pedido.objects.filter(
        status__iexact='separando'
    ).count()

    # Filtra a quantidade de pedidos pendentes
    quantidade_pedidos_pendentes = Pedido.objects.filter(
        status__iexact='aprovados'
    ).count()


    context = {
        'pedidos_finalizados': pedidos_finalizados,
        'quantidade_pedidos_total': quantidade_pedidos_total,
        'quantidade_pedidos_prontos': quantidade_pedidos_prontos,
        'quantidade_pedidos_separacao': quantidade_pedidos_separacao,
        'quantidade_pedidos_pendentes': quantidade_pedidos_pendentes,
        'esse_mes': esse_mes
    }

    return render(request, 'dashboard/index.html', context)
