from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizar_estoque, name='visualizar_estoque'),
]
