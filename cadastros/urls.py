from django.urls import path
from cadastros import views

urlpatterns = [
    path('', views.exbicao_cadastros_produtos_lista, {'modulo': 'Produtos'}, name='home_cadastros'),
    path('produtos/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Produtos'}, name='cadastros_produtos'),
    path('clientes/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Clientes'}, name='cadastros_clientes'),
    path('materiais_de_trabalho/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Materiais de Trabalho'},
         name='cadastro_materiais_de_trabalho'),
    path('fornecedores/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Fornecedores'},
         name='cadastros_fornecedores'),
    path('vendedores/', views.exbicao_cadastros_produtos_lista, {'modulo': 'Vendedores'}, name='cadastros_vendedores'),


    path('cadastrar_novo_produto/', views.ProdutoCreate.as_view(), name='cadastrar_novo_produto'),
    path('exibir_cadastro_produto/', views.exibir_cadastro_produto, name='exibir_cadastro_produto'),

    path('editar_cadastro_produto/<int:pk>', views.ProdutoUpdate.as_view(), name='editar_cadastro_produto'),

    path('deletar_cadastro_produto/<int:pk>', views.ProdutoDelete.as_view(), name='deletar_cadastro_produto'),

    path('listar_produtos/', views.CampoList.as_view(), name='listar_produtos'),
]

