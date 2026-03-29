from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def roles_permitidos(roles_necesarios):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 1. Si no ha iniciado sesión, lo mandamos al login
            if not request.user.is_authenticated:
                messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
                return redirect('login')

            # 2. Si es superusuario (Administrador total de Django), lo dejamos pasar siempre
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # 3. Verificamos si alguno de los roles del usuario coincide con los necesarios
            if request.user.roles.filter(nombre_rol__in=roles_necesarios).exists():
                return view_func(request, *args, **kwargs)

            # 4. Si está logueado pero no tiene el rol (ej. es un ADOPTANTE intentando entrar al admin)
            messages.error(request, "No tienes permisos de administrador o refugio para ver esta sección.")
            return redirect('inicio')

        return _wrapped_view

    return decorator