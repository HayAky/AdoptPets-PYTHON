from django.urls import path
from . import views

urlpatterns = [
    # Rutas de Administración
    path('admin/lista/', views.admin_lista_adopciones, name='admin_lista_adopciones'),
    path('admin/detalle/<int:adopcion_id>/', views.admin_detalle_adopcion, name='admin_detalle_adopcion'),

    # Ruta Pública / Adoptante
    path('solicitar/<int:mascota_id>/', views.solicitar_adopcion, name='solicitar_adopcion'),
    path('admin/detalle/<int:adopcion_id>/seguimiento/nuevo/', views.crear_seguimiento, name='crear_seguimiento'),
    path('panel-solicitudes/', views.panel_solicitudes, name='panel_solicitudes'),
    path('historial/', views.historial_adopciones, name='historial_adopciones'),
    path('solicitud/<int:adopcion_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('solicitud/<int:adopcion_id>/procesar/<str:accion>/', views.procesar_solicitud, name='procesar_solicitud'),
]