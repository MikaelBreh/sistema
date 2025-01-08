from django.urls import path
from . import views

urlpatterns = [
    # path('', views.visualizar_estoque, name='visualizar_estoque'),
    path('necessidade_pedidos/', views.necessidade_pedidos, name='visualizar_necessidade_pedidos_estoque'),
    path('pesquisar_lote/', views.pesquisar_lote, name='pesquisar_lote'),
    path('lote/<str:lote>/', views.estoque_lotes, name='estoque_lotes'),
    path('inventarios_estoque/', views.inventarios_estoque, name='inventarios_estoque'),
    path('criar_inventario_estoque/', views.criar_inventario_estoque, name='criar_inventario_estoque'),
    path('visualizar_inventario_estoque/<int:inventario_id>/', views.visualizar_inventario_estoque, name='visualizar_inventario_estoque'),
    path('editar_inventario_estoque/<int:inventario_id>/', views.editar_inventario_estoque, name='editar_inventario_estoque'),

    path('nova_view_estoque/', views.nova_view_estoque, name='nova_view_estoque'),

    # consultas que vem do estoque
    path('consultas/detalhar_quantidade_separada/<product_code>/', views.detalhar_quantidade_separada, name='detalhar_quantidade_separada'),
    path('consultas/detalhar_pedidos_separar/<product_code>/', views.detalhar_pedidos_separar, name='detalhar_pedidos_separar'),

]


