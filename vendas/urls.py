from django.urls import path
from vendas import views

urlpatterns = [
    path('', views.home, name='vendas_home'),
    path('api/produtos_cliente/<int:cliente_id>/', views.get_produtos_cliente, name='get_produtos_cliente'),

    path('listar_pedidos', views.listar_pedidos, name='listar_pedidos'),
    path('criar_pedido_separacao', views.criar_pedido_separacao, name='criar_pedido_separacao'),
    path('visualizar_pedido/<int:pedido_id>/', views.visualizar_pedido, name='visualizar_pedido'),
    path('editar_pedido/<int:pedido_id>/', views.editar_pedido, name='editar_pedido'),
    path('listar_pedidos_para_gestao/', views.listar_pedidos, {'opcao': 'gestao'}, name='listar_pedidos_para_gestao'),
    path('aprovar_pedido/<int:pedido_id>/', views.aprovar_pedido, name='aprovar_pedido'),
]