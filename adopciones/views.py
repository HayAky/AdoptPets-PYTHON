from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Adopcion, Seguimiento
from mascotas.models import Mascota
from usuarios.decorators import roles_permitidos
from django.utils import timezone


# =========================================================
# GESTIÓN DE ADOPCIONES (Admin y Refugios)
# =========================================================

@roles_permitidos(['ADMIN', 'REFUGIO'])
def admin_lista_adopciones(request):
    # Traemos todas las adopciones, de la más reciente a la más antigua
    adopciones = Adopcion.objects.all().order_by('-fecha_solicitud')
    return render(request, 'adopciones/admin_lista.html', {'adopciones': adopciones})


@roles_permitidos(['ADOPTANTE'])
def solicitar_adopcion(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)

    if mascota.estado_adopcion != 'disponible':
        messages.error(request, 'Lo sentimos, esta mascota ya está en proceso de adopción.')
        return redirect('lista_mascotas')

    solicitud_existente = Adopcion.objects.filter(adoptante=request.user, mascota=mascota,
                                                  estado_adopcion='pendiente').exists()
    if solicitud_existente:
        messages.warning(request, 'Ya tienes una solicitud pendiente para esta mascota.')
        return redirect('lista_mascotas')

    try:  # <-- BLINDAJE
        Adopcion.objects.create(
            adoptante=request.user,
            mascota=mascota,
            estado_adopcion='pendiente',
            fecha_solicitud=timezone.now(),
        )
        mascota.estado_adopcion = 'pendiente'
        mascota.save()
        messages.success(request, f'¡Felicidades! Tu solicitud para adoptar a {mascota.nombre} ha sido enviada.')
    except Exception as e:
        messages.error(request, f'Error al procesar la solicitud: {str(e)}')

    return redirect('lista_mascotas')


@roles_permitidos(['ADMIN', 'REFUGIO'])
def admin_detalle_adopcion(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id_adopcion=adopcion_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')

        try:  # <-- BLINDAJE
            adopcion.estado_adopcion = nuevo_estado
            if nuevo_estado == 'aprobada':
                adopcion.mascota.estado_adopcion = 'adoptado'
                messages.success(request, '¡Adopción APROBADA! La mascota ahora tiene una familia.')
            elif nuevo_estado == 'rechazada':
                adopcion.mascota.estado_adopcion = 'disponible'
                messages.warning(request, 'Solicitud rechazada. La mascota vuelve a estar disponible.')

            adopcion.mascota.save()
            adopcion.save()
        except Exception as e:
            messages.error(request, f'No se pudo cambiar el estado de la adopción: {str(e)}')

        return redirect('admin_lista_adopciones')

    return render(request, 'adopciones/admin_detalle.html', {'adopcion': adopcion})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def crear_seguimiento(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id_adopcion=adopcion_id)

    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None
    if not request.user.es_admin and adopcion.mascota.refugio != mi_refugio:
        messages.error(request, 'Acceso denegado: Esta mascota no pertenece a tu refugio.')
        return redirect('admin_lista_adopciones')

    if request.method == 'POST':
        try:
            Seguimiento.objects.create(
                adopcion=adopcion,
                tipo_contacto=request.POST.get('tipo_contacto'),
                estado_bienestar=request.POST.get('estado_bienestar'),
                observaciones=request.POST.get('observaciones') or None,
                proxima_fecha=request.POST.get('proxima_fecha') or None
            )
            messages.success(request, '¡Bitácora de seguimiento guardada correctamente!')
            # Redirigimos de vuelta a los detalles de esa adopción específica
            return redirect('admin_detalle_adopcion', adopcion_id=adopcion.id_adopcion)

        except Exception as e:
            messages.error(request, f'Error al guardar el seguimiento: {str(e)}')

    context = {
        'adopcion': adopcion,
        'tipos_contacto': Seguimiento.TIPO_CONTACTO_CHOICES,
        'estados_bienestar': Seguimiento.ESTADO_BIENESTAR_CHOICES
    }
    return render(request, 'adopciones/form_seguimiento.html', context)