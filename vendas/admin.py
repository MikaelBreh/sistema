from django.contrib import admin
from .models import Pedido, PedidoItem, PedidoSeparacao


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoItemInline]


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoSeparacao)
