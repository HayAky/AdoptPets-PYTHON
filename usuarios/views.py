from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Usuario, Rol
from mascotas.models import Mascota
from refugios.models import Refugio
from adopciones.models import Adopcion
from .decorators import roles_permitidos


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

def registro(request):
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fechaNacimiento')

        # 1. Validar contraseñas
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        # 2. Validar que el correo no exista
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado. Por favor, inicia sesión.')
            return redirect('registro')

        # 3. Crear el usuario (create_user se encarga de encriptar el password)
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

        # 4. Asignar rol por defecto (Adoptante)
        # get_or_create asegura que si el rol no existe en MySQL, lo crea en ese momento
        rol_adoptante, created = Rol.objects.get_or_create(nombre_rol='ADOPTANTE')
        user.roles.add(rol_adoptante)

        # 5. Iniciar sesión automáticamente y redirigir al inicio
        login(request, user)
        return redirect('inicio')

    # Si la petición es GET (solo entrar a la página), mostramos el formulario
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

    # --- 2. Listas Recientes para las tablas pequeñas ---
    # Traemos las adopciones pendientes, ordenadas de la más antigua a la más nueva
    adopciones_pendientes_lista = Adopcion.objects.filter(estado_adopcion='pendiente').order_by('fecha_solicitud')[:5]

    # Traemos las últimas 5 mascotas registradas que estén disponibles
    ultimas_mascotas = Mascota.objects.filter(estado_adopcion='disponible').order_by('-fecha_registro')[:5]

    # --- 3. Empaquetar el contexto ---
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