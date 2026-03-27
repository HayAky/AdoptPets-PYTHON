from django.urls import path
from . import views

urlpatterns = [
    # Cuando alguien entre a /mascotas/, se ejecutará la vista lista_mascotas
    path('', views.lista_mascotas, name='lista_mascotas'),
]