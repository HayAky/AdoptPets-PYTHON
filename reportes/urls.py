from django.urls import path
from . import views

urlpatterns = [
    # Panel principal
    path('panel/', views.panel_reportes, name='panel_reportes'),

    # Descargas PDF
    path('descargar/mascotas/', views.pdf_mascotas, name='pdf_mascotas'),
    path('descargar/adopciones/', views.pdf_adopciones, name='pdf_adopciones'),
    path('descargar/usuarios/', views.pdf_usuarios, name='pdf_usuarios'),
    path('descargar/refugios/', views.pdf_refugios, name='pdf_refugios'),  # <-- NUEVO
]