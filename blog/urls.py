from django.urls import path
from . import views

urlpatterns = [
    # Vista Pública
    path('', views.lista_blogs, name='lista_blogs'),

    # Rutas CRUD de Administración y Refugio
    path('admin/lista/', views.admin_lista_blogs, name='admin_lista_blogs'),
    path('admin/nuevo/', views.crear_blog, name='crear_blog'),
    path('admin/editar/<int:blog_id>/', views.editar_blog, name='editar_blog'),
    path('admin/eliminar/<int:blog_id>/', views.eliminar_blog, name='eliminar_blog'),
]