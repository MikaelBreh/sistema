from django.db import models

# Create your models here.
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


class Products(models.Model):
    CATEGORY_CHOICES = [
        ('fabricado', 'Fabricado'),
        ('misto', 'Misto'),
        ('kit', 'Kit'),
        ('kit_variavel', 'Kit Variável'),
        ('materia_prima', 'Matéria Prima'),
    ]

    name = models.CharField(max_length=70)
    product_code = models.CharField(max_length=10, null=True, blank=True)
    product_bar_code = models.CharField(max_length=13, null=True, blank=True)
    box_bar_code = models.CharField(max_length=14, null=True, blank=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=10)
    box_quantity = models.IntegerField(null=True, blank=True)
    gross_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ncm = models.CharField(max_length=14, null=True, blank=True)
    cest = models.CharField(max_length=14, null=True, blank=True)

    pedidos = GenericRelation('vendas.PedidoItem')

    def __str__(self):
        return self.name


# ESSA model é usada para quando temos um produto, porem esse produto tem outro codigo de barras, cod, ncm, cest,
# ou ate mesmo nome
class Products_another_info(models.Model):
    produto_pertence = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    product_code = models.CharField(max_length=10, null=True, blank=True)
    product_bar_code = models.CharField(max_length=13, null=True, blank=True)
    box_bar_code = models.CharField(max_length=14, null=True, blank=True)
    box_quantity = models.IntegerField(null=True, blank=True)
    ncm = models.CharField(max_length=14, null=True, blank=True)
    cest = models.CharField(max_length=14, null=False, blank=False)

    pedidos = GenericRelation('vendas.PedidoItem')

    def __str__(self):
        return self.name + '  | PERTENCE: ' + self.produto_pertence.name + ' - ' + self.produto_pertence.product_code



class Vendedores(models.Model):
    name = models.CharField(max_length=40)
    cpf = models.IntegerField()  # Altere o tipo de campo conforme necessário
    phone = models.IntegerField()  # Altere o tipo de campo conforme necessário
    email = models.EmailField(max_length=40)
    address = models.CharField(max_length=40)
    pix = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.name


class TabelaPreco(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class TabelaPrecoProduto(models.Model):
    tabela_preco = models.ForeignKey(TabelaPreco, on_delete=models.CASCADE)
    produto = models.ForeignKey(Products, on_delete=models.CASCADE)
    valor_sem_impostos = models.DecimalField(max_digits=5, decimal_places=2)
    comissao_gerente_comercial = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    comissao_vendedor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    comissao_vendedor2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.tabela_preco.nome} - {self.produto.name} - {self.valor_sem_impostos} -" \
               f" {self.comissao_gerente_comercial} - {self.comissao_vendedor} - {self.comissao_vendedor2}"


class Clientes(models.Model):
    REGIME_CHOICES = [
        ('simples', 'Simples'),
        ('normal', 'Normal'),
    ]

    NOTA_CHOICES = [
        ('nota cheia', 'Nota Cheia'),
        ('meia nota', 'Meia Nota'),
        ('1/3 nota', '1/3 Nota'),
        ('70% valor 70% quantidade', '70% Valor 70% Quantidade')
    ]

    name = models.CharField(max_length=40)
    regime = models.CharField(max_length=10, choices=REGIME_CHOICES)
    cnpj = models.IntegerField()  # Altere o tipo de campo conforme necessário
    ie = models.IntegerField()
    cep = models.IntegerField()  # Altere o tipo de campo conforme necessário
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=40)
    rua = models.CharField(max_length=45)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50)
    nota_fiscal = models.CharField(max_length=24, choices=NOTA_CHOICES)
    TabelaPreco = models.ForeignKey(TabelaPreco, on_delete=models.PROTECT, null=True, blank=True)
    vendedor = models.ForeignKey(Vendedores, on_delete=models.PROTECT, related_name='vendedor', null=True, blank=True)
    vendedor_2 = models.ForeignKey(Vendedores, on_delete=models.PROTECT, related_name='vendedor_adjunto', null=True,
                                   blank=True)
    Gerente_comercial = models.ForeignKey(Vendedores, on_delete=models.PROTECT, related_name='gerente_comercial',
                                          null=True, blank=True)

    def __str__(self):
        return self.name


class Fornecedores(models.Model):
    name = models.CharField(max_length=40)
    cnpj = models.IntegerField()  # Altere o tipo de campo conforme necessário
    cep = models.IntegerField()  # Altere o tipo de campo conforme necessário
    phone = models.IntegerField()  # Altere o tipo de campo conforme necessário
    email = models.EmailField(max_length=40)
    address = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Materiais_de_Trabalho(models.Model):
    name = models.CharField(max_length=40)
    unit = models.CharField(max_length=10)
    supplier = models.ForeignKey(Fornecedores, on_delete=models.CASCADE)
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.name
