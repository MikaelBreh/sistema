from cadastros.models import Products_another_info
from vendas.models import Pedido, PedidoSeparacao

from collections import defaultdict
from django.db.models import Exists, OuterRef

