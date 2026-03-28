from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_adopciones, name='lista_adopciones'),
]