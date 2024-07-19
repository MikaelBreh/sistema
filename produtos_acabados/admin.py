from django.contrib import admin

from produtos_acabados.models import TransferenciaEstoqueSaidaInfo, TransferenciaEstoqueSaidaProdutos

# Register your models here.
admin.site.register(TransferenciaEstoqueSaidaInfo)
admin.site.register(TransferenciaEstoqueSaidaProdutos)