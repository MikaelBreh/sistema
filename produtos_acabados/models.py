from django.db import models
from cadastros.models import Products  # Importe corretamente o modelo Products

class TransferenciaEstoqueSaidaInfo(models.Model):
    numero_transferencia = models.AutoField(primary_key=True)
    data_saida = models.DateField(auto_now_add=True)
    motorista = models.CharField(max_length=40)
    veiculo = models.CharField(max_length=40)
    conferente = models.CharField(max_length=40)
    quantidade_pallets = models.IntegerField()
    observacoes = models.TextField()

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


