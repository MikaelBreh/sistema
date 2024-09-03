import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models
from cadastros.models import Products, Products_another_info  # Importe corretamente o modelo Products
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


class TransferenciaEstoqueSaidaInfo(models.Model):
    numero_transferencia = models.AutoField(primary_key=True)
    data_saida = models.DateField(auto_now_add=True)
    motorista = models.CharField(max_length=40)
    veiculo = models.CharField(max_length=40)
    conferente = models.CharField(max_length=40)
    quantidade_pallets = models.IntegerField()
    observacoes = models.TextField()
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f'Numero Transferencia: {self.numero_transferencia}  Data: {self.data_saida}'

class TransferenciaEstoqueSaidaProdutos(models.Model):
    numero_transferencia = models.ForeignKey(TransferenciaEstoqueSaidaInfo, on_delete=models.CASCADE)
    produto = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantidade_unitaria = models.IntegerField()
    quantidade_caixa = models.IntegerField()
    lote = models.CharField(max_length=20)
    data_fabricacao = models.DateField()
    validade = models.DateField()
    codigo_barra_unidade = models.CharField(max_length=13)
    codigo_barra_caixa = models.CharField(max_length=14)

    def __str__(self):
        return f'{self.produto.name}  | Lote:  {self.lote}   | Data Transferencia:  {self.numero_transferencia.data_saida}'



class MistoItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    produto_misto = GenericForeignKey('content_type', 'object_id')
    produto_nome = models.CharField(max_length=70, default='nat')
    lote = models.CharField(max_length=20)
    quantidade_unitaria = models.IntegerField()
    quantidade_de_caixas = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.produto_misto} - Lote: {self.lote}"

class MistoComponent(models.Model):
    misto_item = models.ForeignKey(MistoItem, related_name='components', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
    object_id = models.PositiveIntegerField()
    produto = GenericForeignKey('content_type', 'object_id')
    lote = models.CharField(max_length=20)
    quantidade = models.IntegerField()

    def __str__(self):
        return f"Componente de {self.misto_item}"