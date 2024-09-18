from django.urls import path
from vendas import views

urlpatterns = [
    path('', views.home, name='vendas_home'),
    path('api/produtos_cliente/<int:cliente_id>/', views.get_produtos_cliente, name='get_produtos_cliente'),

    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('criar_pedido_separacao', views.criar_pedido_separacao, name='criar_pedido_separacao'),
    path('visualizar_pedido/<int:pedido_id>/', views.visualizar_pedido, name='visualizar_pedido'),
    path('editar_pedido/<int:pedido_id>/', views.editar_pedido, name='editar_pedido'),
    path('listar_pedidos_para_gestao/', views.listar_pedidos, {'opcao': 'gestao'}, name='listar_pedidos_para_gestao'),
    path('aprovar_pedido/<int:pedido_id>/', views.aprovar_pedido, name='aprovar_pedido'),

    #  AQUI A NOVA TELA DE PEDIDOS
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),  # Página inicial com o HTML
    path('pedidos/<str:status>/', views.listar_pedidos_por_status, name='listar_pedidos_por_status'),


    # AQUI COMEÇA A PARTE DE EXPEDICAO -- SEPARACAO DE PEDIDOS
    path('expedicao/', views.expedicao_list, name='expedicao_list'),
    path('expedicao/ver/<int:pedido_id>/', views.expedicao_ver, name='expedicao_ver'),
    path('expedicao/separar/<int:pedido_id>/', views.expedicao_separar, name='expedicao_separar'),

    path('expedicao/separando_list_view/', views.expedicao_separando_list_view, name='expedicao_separando_list_view'),
    path('expedicao/separando_ver/<int:pedido_id>/', views.expedicao_ver_separacao, name='expedicao_ver_separacao'),
    path('expedicao/separar_editar/<int:pedido_id>/', views.expedicao_separar_editar, name='expedicao_separar_editar'),


]