from django.urls import path
from vendas import views

urlpatterns = [
    path('', views.home, name='vendas_home'),
    path('api/produtos_cliente/<int:cliente_id>/', views.get_produtos_cliente, name='get_produtos_cliente'),

    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('criar_pedido_separacao/', views.criar_pedido_separacao, name='criar_pedido_separacao'),
    path('visualizar_pedido/<int:pedido_id>/', views.visualizar_pedido, name='visualizar_pedido'),
    path('editar_pedido/<int:pedido_id>/', views.editar_pedido, name='editar_pedido'),

    #  AQUI A NOVA TELA DE PEDIDOS
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/<str:status>/', views.listar_pedidos_por_status, name='listar_pedidos_por_status'),
    path('pedidos/alterar-status/<int:numero_pedido>/<str:novo_status>/', views.alterar_status,
         name='alterar_status_pedido'),

    # Lançar saida do pedido com base no id do pedido
    path('expedicao/lancar_saida/<int:pedido_id>/', views.lancar_saida, name='lancar_saida'),

    path('pedidos/<int:pedido_id>/imprimir/', views.imprimir_conferencia, name='imprimir_conferencia'),


    # AQUI COMEÇA A PARTE DE EXPEDICAO -- SEPARACAO DE PEDIDOS
    path('expedicao/<str:status>', views.expedicao_list, name='expedicao_list'),

    # path('expedicao/ver/<int:pedido_id>/', views.expedicao_ver, name='expedicao_ver'),
    # path('expedicao/separar/<int:pedido_id>/', views.expedicao_separar, name='expedicao_separar'),

    path('expedicao/separando_ver/<int:pedido_id>/', views.expedicao_ver_separacao, name='expedicao_ver_separacao'),
    path('expedicao/separar_editar/<int:pedido_id>/', views.expedicao_separar_editar, name='expedicao_separar_editar'),

    path('expedicao/ver_faltas_pedidos/', views.ver_faltas_pedidos, name='expedicao_ver_faltas_pedidos'),



]