from django.db import models

# Create your models here.
class Products(models.Model):

    CATEGORY_CHOICES = [
        ('fabricado', 'Fabricado'),
        ('kit', 'Kit'),
        ('kit_variavel', 'Kit Variável'),
        ('materia_prima', 'Matéria Prima'),
        # Adicione outras categorias conforme necessário
    ]

    name = models.CharField(max_length=70)
    product_code = models.CharField(max_length=10, null=True, blank=True)
    product_bar_code = models.IntegerField(null=True, blank=True)
    box_bar_code = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=10)
    box_quantity = models.IntegerField(null=True, blank=True)
    gross_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ncm = models.IntegerField(null=True, blank=True)
    cest = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name



class Clientes(models.Model):
    REGIME_CHOICES = [
        ('simples', 'Simples'),
        ('normal', 'Normal'),
    ]

    name = models.CharField(max_length=40)
    regime = models.CharField(max_length=10, choices=REGIME_CHOICES)
    cnpj = models.IntegerField()  # Altere o tipo de campo conforme necessário
    cep = models.IntegerField()  # Altere o tipo de campo conforme necessário

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


class Vendedores(models.Model):
    name = models.CharField(max_length=40)
    cpf = models.IntegerField()  # Altere o tipo de campo conforme necessário
    phone = models.IntegerField()  # Altere o tipo de campo conforme necessário
    email = models.EmailField(max_length=40)
    address = models.CharField(max_length=40)

    def __str__(self):
        return self.name
