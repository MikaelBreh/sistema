from django.urls import path
from cadastros import views

urlpatterns = [
    # esse aqui é o mesmo que o de baixo serve para exibir os produtos como lista
    path('', views.exbicao_cadastros_produtos_lista, {'modulo': 'Produtos'}, name='home_cadastros'),

    # esse codigo exibe os produtos em uma lista, e permite acessar, os de baixo fazem a mesma coisa e usam o mesmo
    # codigo, porem para clientes e vendedores.
    path('produtos/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Produtos'}, name='cadastros_produtos'),
    path('clientes/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Clientes'}, name='cadastros_clientes'),
    #   path('vendedores/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Vendedores'}, name='cadastros_vendedores'),


    path('exibir_cadastro_produto/', views.exibir_cadastro_produto, name='exibir_cadastro_produto'),
    path('exibir_cadastro_cliente/', views.exibir_cadastro_cliente, name='exibir_cadastro_cliente'),

    path('cadastrar_novo_cliente/', views.ClienteCreate.as_view(), name='cadastrar_novo_cliente'),


    # path('materiais_de_trabalho/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Materiais de Trabalho'},
    #      name='cadastro_materiais_de_trabalho'),

    #   path('fornecedores/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Fornecedores'},
    #     name='cadastros_fornecedores'),

    #   path('cadastrar_novo_produto/', views.ProdutoCreate.as_view(), name='cadastrar_novo_produto'),
    #   path('editar_cadastro_produto/<int:pk>', views.ProdutoUpdate.as_view(), name='editar_cadastro_produto'),
    #   path('deletar_cadastro_produto/<int:pk>', views.ProdutoDelete.as_view(), name='deletar_cadastro_produto'),

    #    path('listar_produtos/', views.CampoList.as_view(), name='listar_produtos'),
    # h0nestamente nao sei para que isso ai em cima serve! (: SO A LINHA DE CIMA, O RESTO É IMPORTANTE.
]
