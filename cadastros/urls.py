from django.urls import path
from cadastros import views

urlpatterns = [
    path('', views.home, name='home'),
]