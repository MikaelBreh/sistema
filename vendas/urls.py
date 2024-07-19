from django.urls import path
from vendas import views

urlpatterns = [
    path('', views.home, name='vendas_home'),
    path('api/produtos_cliente/<int:cliente_id>/', views.get_produtos_cliente, name='get_produtos_cliente'),
]