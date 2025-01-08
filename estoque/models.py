from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Estoque(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    fonte = GenericForeignKey('content_type', 'object_id')
    cod_produto = models.CharField(max_length=8, null=True, blank=True)
    lote = models.CharField(max_length=10, null=True, blank=True)
    quantidade = models.IntegerField()
    status = models.BooleanField()
    data = models.DateTimeField(auto_now_add=True)
    inventario = models.BooleanField(default=False)
    id_inventario = models.IntegerField(null=True, blank=True)

    class Meta:
        permissions = [
            ('ver_estoque_por_lotes', 'Can see stock by batches'),
            ('ver_necessidade_pedidos', 'Can see the need for orders'),
            ('ver_inventario_estoque', 'Can see stock inventory')
        ]


    def __str__(self):
        # Acessa a fonte para obter o nome do produto, caso exista
        produto_nome = self.fonte.name if hasattr(self.fonte, 'name') else 'Nome não disponível'
        return f'{self.cod_produto} - {produto_nome} - Lote: {self.lote} - Quant: {self.quantidade}'


class InventariosEstoque(models.Model):
    numero_inventario = models.IntegerField()
    nome_produtos = models.CharField(max_length=60)
    cod_produto = models.CharField(max_length=8, null=True, blank=True)
    lote = models.CharField(max_length=10, null=True, blank=True)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    conferente = models.CharField(max_length=30, null=True, blank=True)
    finalizado = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('ver_inventario_estoque', 'Can see stock inventory'),
            ('editar_inventario_estoque', 'Can edit stock inventory')
        ]

    def __str__(self):
        return f'{self.cod_produto} - Lote: {self.lote} - Quant: {self.quantidade}'