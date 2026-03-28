"""
URL configuration for adopt_pets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views  # <-- Importamos las vistas de auth
from usuarios import views as usuarios_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Al cerrar sesión, redirigimos al login enviando la variable ?logout=true
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/?logout=true'), name='logout'),
    path('register/', usuarios_views.registro, name='registro'),
    # Ruta raíz
    path('', TemplateView.as_view(template_name='main.html'), name='inicio'),

    # Tus aplicaciones
    path('mascotas/', include('mascotas.urls')),
    path('refugios/', include('refugios.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('adopciones/', include('adopciones.urls')),
    path('blog/', include('blog.urls')),
    path('reportes/', include('reportes.urls')),
]