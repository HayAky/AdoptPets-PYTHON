from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Refugio
from usuarios.decorators import roles_permitidos
from mascotas.models import Mascota
from adopciones.models import Adopcion
from usuarios.models import Usuario
from django.db.models import Count, Q

# --- VISTA PÚBLICA ---
from django.db.models import Count, Q


# --- VISTA PÚBLICA (Sin protección) ---
def lista_refugios(request):
    # Traemos todos los refugios activos y contamos cuántas mascotas 'disponibles' tiene cada uno
    refugios = Refugio.objects.filter(activo=True).annotate(
        # Creamos una variable temporal llamada 'mascotas_disponibles_count'
        mascotas_disponibles_count=Count('mascotas', filter=Q(mascotas__estado_adopcion='disponible'))
    ).order_by('nombre_refugio')

    return render(request, 'refugios/lista.html', {'refugios': refugios})
# =========================================================
# VISTAS PROTEGIDAS (Solo Administradores)
# =========================================================

@roles_permitidos(['ADMIN'])
def admin_lista_refugios(request):
    todos_los_refugios = Refugio.objects.all().order_by('-fecha_registro')
    return render(request, 'refugios/admin_lista.html', {'refugios': todos_los_refugios})


@roles_permitidos(['ADMIN'])
def crear_refugio(request):
    # Traemos solo a los usuarios que tienen el rol REFUGIO para no saturar la lista
    usuarios_refugio = Usuario.objects.filter(roles__nombre_rol='REFUGIO', is_active=True)

    if request.method == 'POST':
        guardar_datos_refugio(request, Refugio())
        messages.success(request, 'Refugio creado correctamente.')
        return redirect('admin_lista_refugios')

    return render(request, 'refugios/form.html', {'usuarios_refugio': usuarios_refugio})


@roles_permitidos(['ADMIN'])
def editar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    usuarios_refugio = Usuario.objects.filter(roles__nombre_rol='REFUGIO', is_active=True)

    if request.method == 'POST':
        guardar_datos_refugio(request, refugio)
        messages.success(request, 'Refugio actualizado correctamente.')
        return redirect('admin_lista_refugios')

    return render(request, 'refugios/form.html', {'refugio': refugio, 'usuarios_refugio': usuarios_refugio})

@roles_permitidos(['ADMIN'])
def eliminar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    refugio.delete()
    messages.success(request, 'Refugio eliminado correctamente.')
    return redirect('admin_lista_refugios')


# --- FUNCIÓN AUXILIAR PARA GUARDAR DATOS ---
def guardar_datos_refugio(request, refugio):
    refugio.nombre_refugio = request.POST.get('nombreRefugio')
    refugio.responsable = request.POST.get('responsable')
    refugio.localidad = request.POST.get('localidad')
    refugio.direccion = request.POST.get('direccion')
    refugio.telefono = request.POST.get('telefono')
    refugio.email = request.POST.get('email')
    refugio.capacidad_maxima = request.POST.get('capacidadMaxima') or None
    refugio.descripcion = request.POST.get('descripcion')
    refugio.activo = request.POST.get('activo') == 'on'

    # --- NUEVO: Capturar el usuario encargado ---
    usuario_id = request.POST.get('usuarioEncargado')
    if usuario_id:
        refugio.usuario_encargado_id = usuario_id  # Asignamos por ID
    else:
        refugio.usuario_encargado = None  # Por si lo dejan vacío

    refugio.save()

# =========================================================
# PANEL EXCLUSIVO PARA REFUGIOS
# =========================================================

@roles_permitidos(['REFUGIO'])
def dashboard_refugio(request):
    # 1. Buscamos cuál es el refugio de este usuario
    try:
        mi_refugio = request.user.mi_refugio
    except:
        messages.error(request, "Tu cuenta no tiene un refugio físico asignado. Contacta al administrador.")
        return redirect('inicio')

    # 2. Buscamos SOLO las mascotas de ESTE refugio
    mis_mascotas = Mascota.objects.filter(refugio=mi_refugio)
    mascotas_disponibles = mis_mascotas.filter(estado_adopcion='disponible').count()

    # 3. Buscamos SOLO las solicitudes de adopción de ESTAS mascotas
    # Usamos la sintaxis de doble guion bajo (mascota__refugio) para navegar entre tablas
    mis_solicitudes = Adopcion.objects.filter(mascota__refugio=mi_refugio)
    solicitudes_pendientes = mis_solicitudes.filter(estado_adopcion='pendiente').order_by('-fecha_solicitud')
    adopciones_aprobadas = mis_solicitudes.filter(estado_adopcion='aprobada').count()

    context = {
        'refugio': mi_refugio,
        'totalMascotas': mis_mascotas.count(),
        'mascotasDisponibles': mascotas_disponibles,
        'pendientesCount': solicitudes_pendientes.count(),
        'aprobadasCount': adopciones_aprobadas,
        'solicitudesPendientes': solicitudes_pendientes[:5]  # Solo mostramos las últimas 5 en el panel
    }

    return render(request, 'refugios/dashboard_refugio.html', context)