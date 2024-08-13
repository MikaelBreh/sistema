from django.contrib import admin

from .models import TransferenciaEstoqueSaidaInfo, TransferenciaEstoqueSaidaProdutos, MistoItem, MistoComponent

# Register your models here.
admin.site.register(TransferenciaEstoqueSaidaInfo)
admin.site.register(TransferenciaEstoqueSaidaProdutos)
admin.site.register(MistoItem)
admin.site.register(MistoComponent)
