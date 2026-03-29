from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Adopcion
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


@roles_permitidos(['ADMIN', 'REFUGIO'])
def admin_detalle_adopcion(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id_adopcion=adopcion_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # 'aprobada' o 'rechazada'
        observaciones = request.POST.get('observaciones', '')

        # Actualizamos la adopción
        adopcion.estado_adopcion = nuevo_estado

        # Si tu modelo tiene un campo de observaciones, lo guardamos (opcional)
        # adopcion.observaciones = observaciones

        # REGLA DE NEGOCIO: Si se aprueba, la mascota pasa a estar "adoptado"
        if nuevo_estado == 'aprobada':
            adopcion.mascota.estado_adopcion = 'adoptado'
            adopcion.mascota.save()
            messages.success(request, '¡Adopción APROBADA! La mascota ahora tiene una familia.')

        elif nuevo_estado == 'rechazada':
            # Si se rechaza, aseguramos que la mascota vuelva a estar disponible
            adopcion.mascota.estado_adopcion = 'disponible'
            adopcion.mascota.save()
            messages.warning(request, 'Solicitud rechazada. La mascota vuelve a estar disponible.')

        adopcion.save()
        return redirect('admin_lista_adopciones')

    return render(request, 'adopciones/admin_detalle.html', {'adopcion': adopcion})


@roles_permitidos(['ADOPTANTE'])
def solicitar_adopcion(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)

    # Verificamos que la mascota siga disponible por si alguien más la pidió hace un minuto
    if mascota.estado_adopcion != 'disponible':
        messages.error(request, 'Lo sentimos, esta mascota ya está en proceso de adopción con otra familia.')
        return redirect('lista_mascotas')

    # Evitamos que el mismo usuario envíe dos solicitudes para la misma mascota
    solicitud_existente = Adopcion.objects.filter(adoptante=request.user, mascota=mascota,
                                                  estado_adopcion='pendiente').exists()
    if solicitud_existente:
        messages.warning(request, 'Ya tienes una solicitud pendiente para esta mascota.')
        return redirect('lista_mascotas')

    # Creamos la solicitud en MySQL
    Adopcion.objects.create(
        adoptante=request.user,
        mascota=mascota,
        estado_adopcion='pendiente',
        fecha_solicitud=timezone.now(),
    )

    # Cambiamos el estado de la mascota a "Pendiente" para que desaparezca de la vitrina pública
    mascota.estado_adopcion = 'pendiente'
    mascota.save()

    messages.success(request,
                     f'¡Felicidades! Tu solicitud para adoptar a {mascota.nombre} ha sido enviada al administrador. Nos pondremos en contacto contigo pronto.')
    return redirect('lista_mascotas')