from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Refugio
from usuarios.decorators import roles_permitidos
from mascotas.models import Mascota
from adopciones.models import Adopcion
from usuarios.models import Usuario
from django.db.models import Count, Q

def lista_refugios(request):
    refugios = Refugio.objects.filter(activo=True).annotate(
        mascotas_disponibles_count=Count('mascotas', filter=Q(mascotas__estado_adopcion='disponible'))
    ).order_by('nombre_refugio')

    return render(request, 'refugios/lista.html', {'refugios': refugios})


@roles_permitidos(['ADMIN'])
def admin_lista_refugios(request):
    todos_los_refugios = Refugio.objects.all().order_by('-fecha_registro')
    return render(request, 'refugios/admin_lista.html', {'refugios': todos_los_refugios})


@roles_permitidos(['ADMIN'])
def crear_refugio(request):
    usuarios_refugio = Usuario.objects.filter(roles__nombre_rol='REFUGIO', is_active=True)
    if request.method == 'POST':
        try:  # <-- BLINDAJE
            guardar_datos_refugio(request, Refugio())
            messages.success(request, 'Refugio creado correctamente.')
            return redirect('admin_lista_refugios')
        except Exception as e:
            messages.error(request, f'Error al crear el refugio: {str(e)}')

    return render(request, 'refugios/form.html', {'usuarios_refugio': usuarios_refugio})


@roles_permitidos(['ADMIN'])
def editar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    usuarios_refugio = Usuario.objects.filter(roles__nombre_rol='REFUGIO', is_active=True)
    if request.method == 'POST':
        try:  # <-- BLINDAJE
            guardar_datos_refugio(request, refugio)
            messages.success(request, 'Refugio actualizado correctamente.')
            return redirect('admin_lista_refugios')
        except Exception as e:
            messages.error(request, f'Error al actualizar el refugio: {str(e)}')

    return render(request, 'refugios/form.html', {'refugio': refugio, 'usuarios_refugio': usuarios_refugio})


@roles_permitidos(['ADMIN'])
def eliminar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    try:  # <-- BLINDAJE CRÍTICO
        refugio.delete()
        messages.success(request, 'Refugio eliminado correctamente.')
    except Exception as e:
        messages.error(request, 'No puedes eliminar este refugio porque tiene mascotas o procesos vinculados a él.')

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

    usuario_id = request.POST.get('usuarioEncargado')
    if usuario_id:
        refugio.usuario_encargado_id = usuario_id
    else:
        refugio.usuario_encargado = None

    refugio.save()



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