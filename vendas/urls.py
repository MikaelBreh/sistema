from django.urls import path
from vendas import views

urlpatterns = [
    path('', views.home, name='vendas_home'),
]