from django.urls import path
from . import views

urlpatterns = [
    # Rutas CRUD de Administración
    path('admin/lista/', views.admin_lista_usuarios, name='admin_lista_usuarios'),
    path('admin/nuevo/', views.crear_usuario, name='crear_usuario'),  # <-- NUEVA RUTA
    path('admin/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('admin/resetear-password/<int:usuario_id>/', views.resetear_password, name='resetear_password'),
    path('admin/toggle/<int:usuario_id>/', views.toggle_usuario, name='toggle_usuario'),

    # Rutas de Adoptante
    path('perfil/', views.perfil_adoptante, name='perfil_adoptante'),
]