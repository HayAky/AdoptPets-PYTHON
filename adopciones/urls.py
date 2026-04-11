from django.urls import path
from . import views

urlpatterns = [
    # Rutas de Administración
    path('admin/lista/', views.admin_lista_adopciones, name='admin_lista_adopciones'),
    path('admin/detalle/<int:adopcion_id>/', views.admin_detalle_adopcion, name='admin_detalle_adopcion'),

    # Ruta Pública / Adoptante
    path('solicitar/<int:mascota_id>/', views.solicitar_adopcion, name='solicitar_adopcion'),
    path('admin/detalle/<int:adopcion_id>/seguimiento/nuevo/', views.crear_seguimiento, name='crear_seguimiento'),
]