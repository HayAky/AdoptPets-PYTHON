from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Usuario, Rol
from mascotas.models import Mascota
from refugios.models import Refugio
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from adopciones.models import Adopcion
from .decorators import roles_permitidos
from django.shortcuts import render, redirect, get_object_or_404

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fechaNacimiento')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado. Por favor, inicia sesión.')
            return redirect('registro')
        try:
            user = Usuario.objects.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                password=password,
                direccion=direccion,
                telefono=telefono,
                cedula=cedula,
                fecha_nacimiento=fecha_nacimiento
            )

            rol_adoptante, created = Rol.objects.get_or_create(nombre_rol='ADOPTANTE')
            user.roles.add(rol_adoptante)


            login(request, user)
            messages.success(request, '¡Bienvenido a AdoptPets! Tu cuenta ha sido creada.')
            return redirect('inicio')

        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al crear tu cuenta: {str(e)}')
            return redirect('registro')

    return render(request, 'register.html')

@roles_permitidos(['ADMIN'])
def admin_dashboard(request):
    # --- 1. Estadísticas Generales (Contadores) ---
    total_mascotas = Mascota.objects.count()
    mascotas_disponibles = Mascota.objects.filter(estado_adopcion='disponible').count()

    solicitudes_pendientes = Adopcion.objects.filter(estado_adopcion='pendiente').count()
    adopciones_completadas = Adopcion.objects.filter(estado_adopcion='adoptado').count()

    total_usuarios = Usuario.objects.count()
    total_refugios = Refugio.objects.count()


    adopciones_pendientes_lista = Adopcion.objects.filter(estado_adopcion='pendiente').order_by('fecha_solicitud')[:5]


    ultimas_mascotas = Mascota.objects.filter(estado_adopcion='disponible').order_by('-fecha_registro')[:5]

    context = {
        'totalMascotas': total_mascotas,
        'mascotasDisponibles': mascotas_disponibles,
        'solicitudesPendientes': solicitudes_pendientes,
        'adopcionesCompletadas': adopciones_completadas,
        'totalUsuarios': total_usuarios,
        'totalRefugios': total_refugios,
        'adopcionesPendientes': adopciones_pendientes_lista,
        'ultimasMascotas': ultimas_mascotas
    }

    return render(request, 'admin/dashboard.html', context)


@roles_permitidos(['ADMIN'])
def admin_lista_usuarios(request):
    todos_los_usuarios = Usuario.objects.all().prefetch_related('roles')

    adoptantes = todos_los_usuarios.filter(roles__nombre_rol='ADOPTANTE').distinct()
    refugios = todos_los_usuarios.filter(roles__nombre_rol='REFUGIO').distinct()


    cantidad_activos = todos_los_usuarios.filter(is_active=True).count()

    context = {
        'usuarios': todos_los_usuarios,
        'adoptantes': adoptantes,
        'listaRefugios': refugios,
        'cantidadActivos': cantidad_activos,
        'cantidadAdoptantes': adoptantes.count(),
        'cantidadRefugios': refugios.count(),
    }
    return render(request, 'usuarios/admin_lista.html', context)


@roles_permitidos(['ADMIN'])
def crear_usuario(request):
    todos_los_roles = Rol.objects.all()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula') or None
        telefono = request.POST.get('telefono') or None
        ciudad = request.POST.get('ciudad') or None
        direccion = request.POST.get('direccion') or None

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, f'Error: El correo {email} ya está registrado.')
            return redirect('crear_usuario')

        # 2
        try:
            usuario = Usuario.objects.create_user(
                email=email,
                nombre=nombre,
                apellido=apellido,
                password=password,
                cedula=cedula,
                telefono=telefono,
                ciudad=ciudad,
                direccion=direccion
            )

            roles_ids = request.POST.getlist('rolesIds')
            if roles_ids:
                for rol_id in roles_ids:
                    rol = Rol.objects.get(id_rol=rol_id)
                    usuario.roles.add(rol)

            messages.success(request, f'Usuario {nombre} {apellido} creado exitosamente.')
            return redirect('admin_lista_usuarios')

        except Exception as e:
            messages.error(request, f'Error al intentar guardar el usuario en la base de datos: {str(e)}')

    context = {
        'todosLosRoles': todos_los_roles,
        'roles_usuario_ids': []
    }
    return render(request, 'usuarios/form.html', context)


@roles_permitidos(['ADMIN'])
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    todos_los_roles = Rol.objects.all()

    if request.method == 'POST':
        try:
            usuario.nombre = request.POST.get('nombre')
            usuario.apellido = request.POST.get('apellido')
            usuario.cedula = request.POST.get('cedula') or None
            usuario.fecha_nacimiento = request.POST.get('fechaNacimiento') or None
            usuario.telefono = request.POST.get('telefono') or None
            usuario.ciudad = request.POST.get('ciudad') or None
            usuario.direccion = request.POST.get('direccion') or None
            usuario.is_active = request.POST.get('activo') == 'on'
            usuario.save()

            roles_ids = request.POST.getlist('rolesIds')
            if roles_ids:
                usuario.roles.clear()
                for rol_id in roles_ids:
                    rol = Rol.objects.get(id_rol=rol_id)
                    usuario.roles.add(rol)

            messages.success(request, 'Usuario actualizado exitosamente')
            return redirect('admin_lista_usuarios')

        except Exception as e:
            messages.error(request, f'Error al actualizar los datos: {str(e)}')

    context = {
        'usuario': usuario,
        'todosLosRoles': todos_los_roles,
        'roles_usuario_ids': list(usuario.roles.values_list('id_rol', flat=True))
    }
    return render(request, 'usuarios/form.html', context)


@roles_permitidos(['ADMIN'])
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

    if request.user.id_usuario == usuario.id_usuario:
        messages.error(request, 'No puedes eliminar tu propia cuenta de administrador.')
        return redirect('admin_lista_usuarios')

    try:  # <--- BLINDAJE
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
    except Exception as e:
        # Aquí el error suele ser de "Integridad Referencial" (llaves foráneas)
        messages.error(request,
                       'No se puede eliminar este usuario porque tiene registros importantes vinculados (adopciones, mascotas a cargo, etc.).')

    return redirect('admin_lista_usuarios')

@roles_permitidos(['ADMIN'])
def resetear_password(request, usuario_id):
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    usuario.set_password('123456')
    usuario.save()
    messages.success(request, f'Contraseña de {usuario.nombre} reseteada a: 123456')
    return redirect(request.META.get('HTTP_REFERER', 'admin_lista_usuarios'))


@roles_permitidos(['ADMIN'])
def toggle_usuario(request, usuario_id):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
        if request.user.id_usuario == usuario.id_usuario:
            messages.error(request, 'No puedes desactivar tu propia cuenta.')
        else:
            usuario.is_active = not usuario.is_active
            usuario.save()
            estado = "activado" if usuario.is_active else "desactivado"
            messages.success(request, f'Usuario {estado} exitosamente.')
    return redirect('admin_lista_usuarios')


@roles_permitidos(['ADOPTANTE'])
def perfil_adoptante(request):
    usuario = request.user

    if request.method == 'POST':
        try:
            usuario.nombre = request.POST.get('nombre')
            usuario.apellido = request.POST.get('apellido')
            usuario.telefono = request.POST.get('telefono')
            usuario.direccion = request.POST.get('direccion')
            usuario.ciudad = request.POST.get('ciudad')
            usuario.cedula = request.POST.get('cedula') or usuario.cedula
            usuario.save()
            messages.success(request, 'Tus datos han sido actualizados correctamente.')
            return redirect('perfil_adoptante')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar tu perfil: {str(e)}')

    mis_adopciones = Adopcion.objects.filter(adoptante=usuario).order_by('-fecha_solicitud')
    return render(request, 'usuarios/perfil_adoptante.html', {'mis_adopciones': mis_adopciones})