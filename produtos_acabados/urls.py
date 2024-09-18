from django.urls import path
from . import views
from .views import lista_produtos_estoque

urlpatterns = [

    # abaixo as urls para dar entradas(inicio) nas transferencias de estoque

    path('', views.listar_transferencias_estoque, name='listar_transferencias_estoque'),
    path('entrada_produtos_acabados/', views.entrada_produtos_acabados, name='entrada_produtos_acabados'),
    path('listar_transferencias_estoque/', views.listar_transferencias_estoque, name='listar_transferencias_estoque'),
    path('exibir_transferencias_estoque/', views.exibir_transferencias_estoque, name='exibir_transferencia_estoque'),
    path('adicionar_produto_transferencia/', views.adicionar_produto_transferencia, name='adicionar_produto_transferencia'),

    # abaixo as urls para conferencia de transferencias

    path('listar_transferencias_para_conferencia/', views.listar_transferecias_para_conferencia,
         name='listar_transferecias_para_conferencia'),
    path('receber_transferencia_estoque/', views.receber_transferencia_estoque, name='receber_transferencia_estoque'),
    path('entradas_recebidas_estoque/', views.listar_transferencias_recebidas, name='entradas_recebidas_estoque'),
    path('estoque_produtos_pa/', lista_produtos_estoque, name='lista_produtos_estoque'),

    # abaixo as urls para misto de produtos

    path('create-misto-item/', views.create_misto_item, name='create_misto_item'),
    path('listar_mistos_criados/', views.list_item_misto, name='list_misto_item'),
    path('visualizar_misto_item/<int:misto_pk>/', views.visualizar_misto_item, name='visualizar_misto_item'),


]
