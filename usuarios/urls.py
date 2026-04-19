from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # <-- Agrega esta importación arriba
from django.urls import reverse_lazy

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
    path('recuperar/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset.html',
        email_template_name='usuarios/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),

    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'
    ), name='password_reset_done'),

    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html'
    ), name='password_reset_complete'),
]