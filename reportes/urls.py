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
# ... debajo de las descargas que ya tenías ...
    path('refugios/excel/', views.reporte_refugios_excel, name='reporte_refugios_excel'),
    path('usuarios/excel/', views.reporte_usuarios_excel, name='reporte_usuarios_excel'),
        path('adopciones/pdf/', views.reporte_adopciones_pdf, name='reporte_adopciones_pdf'),
    path('refugios/pdf/', views.reporte_refugios_pdf, name='reporte_refugios_pdf'),
    path('usuarios/pdf/', views.reporte_usuarios_pdf, name='reporte_usuarios_pdf'),
]