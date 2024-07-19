from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_transferencias_estoque, name='listar_transferencias_estoque'),
    path('entrada_produtos_acabados/', views.entrada_produtos_acabados, name='entrada_produtos_acabados'),
    path('listar_transferencias_estoque/', views.listar_transferencias_estoque, name='listar_transferencias_estoque'),
    path('exibir_transferencias_estoque/', views.exibir_transferencias_estoque, name='exibir_transferencia_estoque'),
    path('listar_transferencias_para_conferencia/', views.listar_transferecias_para_conferencia, name='listar_transferecias_para_conferencia'),
    path('receber_transferencia_estoque/', views.receber_transferencia_estoque, name='receber_transferencia_estoque'),
]
