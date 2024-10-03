from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizar_estoque, name='visualizar_estoque'),
    path('necessidade_pedidos/', views.necessidade_pedidos, name='visualizar_necessidade_pedidos_estoque'),
    path('pesquisar_lote/', views.pesquisar_lote, name='pesquisar_lote'),
    path('lote/<str:lote>/', views.estoque_lotes, name='estoque_lotes'),
]
