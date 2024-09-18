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
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        # Acessa a fonte para obter o nome do produto, caso exista
        produto_nome = self.fonte.name if hasattr(self.fonte, 'name') else 'Nome não disponível'
        return f'{self.cod_produto} - {produto_nome} - Lote: {self.lote} - Quant: {self.quantidade}'

