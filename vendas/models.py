# models.py
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import date

from cadastros.models import Products, Products_another_info
from cadastros.models import Clientes


class Pedido(models.Model):

    STATUS_CHOICES = [
        ('em_aberto', 'Em Aberto'),
        ('aprovados', 'Aprovados'),
        ('separando', 'Separando'),
        ('conf_separacao', 'Conferência Separação'),
        ('separacao_finalizada', 'Separação Finalizada'),
        ('finalizados', 'Finalizados'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_aberto')
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = [
            ('alterar_status', 'can chance status')
        ]


    def __str__(self):
        return f" {self.cliente} de {self.data.strftime('%d/%m/%Y')} - situação: {self.status}"


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

    class Meta:
        permissions = [
            ('listar_pedidos_separacao', 'can list separations')
        ]

    def __str__(self):
        return f"Pedido: {self.pedido} --- Lote {self.lote} - {self.quantidade} unidades do produto {self.item_pedido.produto}"


# Essa model vai servir para sabermos o que falta das separacoes
class FaltandoSeparacao(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='faltando_separacao', on_delete=models.CASCADE)
    item_pedido = models.ForeignKey(PedidoItem, related_name='faltando_separacao', on_delete=models.CASCADE)
    cod_produto = models.CharField(max_length=20)
    quantidade_pedido = models.PositiveIntegerField()
    quantidade_separada = models.PositiveIntegerField()

    def __str__(self):
        return f"Pedido: {self.pedido} ---pedido {self.quantidade_pedido} - separado: {self.quantidade_separada}  do item: {self.item_pedido.produto}"