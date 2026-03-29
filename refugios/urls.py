from django.urls import path
from . import views

urlpatterns = [
    # Vista pública
    path('', views.lista_refugios, name='lista_refugios'),

    # Rutas CRUD del Administrador...
    path('admin/lista/', views.admin_lista_refugios, name='admin_lista_refugios'),
    path('admin/nuevo/', views.crear_refugio, name='crear_refugio'),
    path('admin/editar/<int:refugio_id>/', views.editar_refugio, name='editar_refugio'),
    path('admin/eliminar/<int:refugio_id>/', views.eliminar_refugio, name='eliminar_refugio'),

    # Rutas del Empleado del Refugio
    path('panel/', views.dashboard_refugio, name='dashboard_refugio'),
]