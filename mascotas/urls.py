from django.urls import path
from . import views

urlpatterns = [
    # Vista pública
    path('', views.lista_mascotas, name='lista_mascotas'),

    # Rutas CRUD de Administración
    # Ahora apunta a la nueva vista
    path('admin/lista/', views.admin_lista_mascotas, name='admin_lista_mascotas'),
    path('admin/nueva/', views.crear_mascota, name='crear_mascota'),
    path('admin/editar/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('admin/eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('detalle/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
# En tu archivo urls.py donde tienes las rutas de mascotas
    path('mascotas/reactivar/<int:mascota_id>/', views.reactivar_mascota, name='reactivar_mascota'),
]