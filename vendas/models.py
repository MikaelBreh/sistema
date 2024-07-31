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

    def __str__(self):
        return f" {self.cliente} de {self.data.strftime('%d/%m/%Y')}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)

    # Campos para a relação genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    produto = GenericForeignKey('content_type', 'object_id')

    quantidade = models.PositiveIntegerField()
    quantidade_caixas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade} of {self.produto}"

