from django.urls import path
from . import views

urlpatterns = [
    # Panel principal
    path('panel/', views.panel_reportes, name='panel_reportes'),

    # Descargas Excel
    path('mascotas/excel/', views.reporte_mascotas_excel, name='reporte_mascotas_excel'),
    path('adopciones/excel/', views.reporte_adopciones_excel, name='reporte_adopciones_excel'),

    # Descargas PDF
    path('mascotas/pdf/', views.reporte_mascotas_pdf, name='reporte_mascotas_pdf'),
]