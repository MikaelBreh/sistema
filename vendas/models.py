# models.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import date

from cadastros.models import Products, Products_another_info
from cadastros.models import Clientes


class Pedido(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    status = models.IntegerField(default=2)

    def __str__(self):
        return f" {self.cliente} de {self.data.strftime('%d/%m/%Y')}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)

    # Campos para a relação genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    produto = GenericForeignKey('content_type', 'object_id')

    quantidade = models.PositiveIntegerField()
    quantidade_caixas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade} of {self.produto}"



class PedidoSeparacao(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='separacoes', on_delete=models.CASCADE)
    item_pedido = models.ForeignKey(PedidoItem, related_name='separacoes', on_delete=models.CASCADE)
    lote = models.CharField(max_length=50)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"Pedido: {self.pedido} --- Lote {self.lote} - {self.quantidade} unidades do produto {self.item_pedido.produto}"
