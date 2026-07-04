from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Refugio
from mascotas.models import Mascota
from adopciones.models import Adopcion
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from usuarios.decorators import roles_permitidos
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RefugioForm, EditUsuarioForm

LOCALIDADES_BOGOTA = [
    "Usaquén", "Chapinero", "Santa Fe", "San Cristóbal", "Usme", "Tunjuelito",
    "Bosa", "Kennedy", "Fontibón", "Engativá", "Suba", "Barrios Unidos",
    "Teusaquillo", "Los Mártires", "Antonio Nariño", "Puente Aranda",
    "La Candelaria", "Rafael Uribe Uribe", "Ciudad Bolívar", "Sumapaz"
]
def lista_refugios(request):
    # Captura de parámetros GET
    nombre_query = request.GET.get('nombre', '')
    localidad_query = request.GET.get('localidad', '')

    # Query base
    refugios = Refugio.objects.filter(activo=True).annotate(
        mascotas_disponibles_count=Count('mascotas', filter=Q(mascotas__estado_adopcion='disponible'))
    ).order_by('nombre_refugio')

    # Aplicar filtros
    if nombre_query:
        refugios = refugios.filter(nombre_refugio__icontains=nombre_query)
    if localidad_query:
        refugios = refugios.filter(localidad=localidad_query)

    return render(request, 'refugios/lista.html', {
        'refugios': refugios,
        'localidades': LOCALIDADES_BOGOTA,
        'nombre_query': nombre_query,
        'localidad_query': localidad_query
    })


@roles_permitidos(['ADMIN'])
def admin_lista_refugios(request):
    # Captura de filtros
    busqueda = request.GET.get('busqueda', '')
    localidad_query = request.GET.get('localidad', '')

    # Query inicial
    todos_los_refugios = Refugio.objects.all().order_by('-fecha_registro')

    # Aplicar filtros
    if busqueda:
        todos_los_refugios = todos_los_refugios.filter(nombre_refugio__icontains=busqueda)
    if localidad_query:
        todos_los_refugios = todos_los_refugios.filter(localidad=localidad_query)

    return render(request, 'refugios/admin_lista.html', {
        'refugios': todos_los_refugios,
        'busqueda': busqueda,
        'localidad_query': localidad_query,
        'localidades': LOCALIDADES_BOGOTA # Asegúrate de que esta lista esté definida en el archivo
    })


@roles_permitidos(['ADMIN'])
def crear_refugio(request):
    if request.method == 'POST':
        form = RefugioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Refugio creado correctamente.')
            return redirect('admin_lista_refugios')
    else:
        form = RefugioForm()
    return render(request, 'refugios/form.html', {'form': form})

@roles_permitidos(['ADMIN'])
def editar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    if request.method == 'POST':
        form = RefugioForm(request.POST, instance=refugio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Refugio actualizado correctamente.')
            return redirect('admin_lista_refugios')
    else:
        form = RefugioForm(instance=refugio)
    return render(request, 'refugios/form.html', {'form': form, 'refugio': refugio})


@roles_permitidos(['ADMIN'])
def eliminar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)

    # En lugar de refugio.delete(), hacemos esto:
    refugio.activo = False
    refugio.save()

    messages.success(request, 'Refugio desactivado correctamente.')
    return redirect('admin_lista_refugios')

@roles_permitidos(['ADMIN'])
def reactivar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    refugio.activo = True
    refugio.save()
    messages.success(request, 'Refugio reactivado correctamente.')
    return redirect('admin_lista_refugios')


@roles_permitidos(['REFUGIO'])
def dashboard_refugio(request):
    try:
        mi_refugio = request.user.mi_refugio
    except:
        messages.error(request, "Tu cuenta no tiene un refugio físico asignado. Contacta al administrador.")
        return redirect('inicio')

    mis_mascotas = Mascota.objects.filter(refugio=mi_refugio)
    mascotas_disponibles = mis_mascotas.filter(estado_adopcion='disponible').count()
    mis_solicitudes = Adopcion.objects.filter(mascota__refugio=mi_refugio)
    solicitudes_pendientes = mis_solicitudes.filter(estado_adopcion='pendiente').order_by('-fecha_solicitud')
    adopciones_aprobadas = mis_solicitudes.filter(estado_adopcion='aprobada').count()

    context = {
        'refugio': mi_refugio,
        'totalMascotas': mis_mascotas.count(),
        'mascotasDisponibles': mascotas_disponibles,
        'pendientesCount': solicitudes_pendientes.count(),
        'aprobadasCount': adopciones_aprobadas,
        'solicitudesPendientes': solicitudes_pendientes[:5]
    }

    return render(request, 'refugios/dashboard_refugio.html', context)


@login_required
@roles_permitidos(['REFUGIO', 'ADMIN'])
def configuracion_refugio(request):
    refugio = request.user.mi_refugio
    usuario = request.user

    # Inicialización de formularios
    form_refugio = RefugioForm(instance=refugio)
    form_usuario = EditUsuarioForm(instance=usuario)
    form_pass = PasswordChangeForm(user=usuario)

    # Dentro de tu función configuracion_refugio en views.py

    if request.method == 'POST':
        if 'btn_refugio' in request.POST:
            form_refugio = RefugioForm(request.POST, instance=refugio)
            if form_refugio.is_valid():
                form_refugio.save()
                messages.success(request, 'Datos del refugio actualizados.')
            else:
                messages.error(request, 'Error al guardar el refugio. Revisa los campos.')

        elif 'btn_usuario' in request.POST:
            form_usuario = EditUsuarioForm(request.POST, instance=usuario)
            if form_usuario.is_valid():
                form_usuario.save()
                messages.success(request, 'Tus datos personales han sido actualizados.')
            else:
                messages.error(request, 'Error en tus datos personales.')
        elif 'btn_pass' in request.POST:
            form_pass = PasswordChangeForm(user=usuario, data=request.POST)
            if form_pass.is_valid():
                user = form_pass.save()
                update_session_auth_hash(request, user)  # Importante para no cerrar sesión
                messages.success(request, 'Contraseña actualizada correctamente.')
            else:
                messages.error(request, 'Error al cambiar la contraseña. Revisa los campos.')

    return render(request, 'refugios/configuracion.html', {
        'form_refugio': form_refugio,
        'form_usuario': form_usuario,
        'form_pass': form_pass
    })
