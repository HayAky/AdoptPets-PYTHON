from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mascota
from refugios.models import Refugio
from django.db.models import Q
from usuarios.decorators import roles_permitidos


def lista_mascotas(request):
    mascotas = Mascota.objects.filter(estado_adopcion='disponible').order_by('-fecha_registro')

    # 1. Capturamos TODOS los posibles filtros de la URL
    busqueda = request.GET.get('busqueda', '')
    especie = request.GET.get('especie', '')
    sexo = request.GET.get('sexo', '')
    tamano = request.GET.get('tamano', '')
    raza = request.GET.get('raza', '')
    edad_min = request.GET.get('edadMin', '')
    edad_max = request.GET.get('edadMax', '')
    vacunado = request.GET.get('vacunado')
    esterilizado = request.GET.get('esterilizado')
    microchip = request.GET.get('microchip')

    if busqueda:
        mascotas = mascotas.filter(Q(nombre__icontains=busqueda) | Q(raza__icontains=busqueda))
    if especie:
        mascotas = mascotas.filter(especie=especie)
    if sexo:
        mascotas = mascotas.filter(sexo=sexo)
    if tamano:
        mascotas = mascotas.filter(tamano=tamano)
    if raza:
        mascotas = mascotas.filter(raza__icontains=raza)  # icontains busca coincidencias parciales

    # Filtros numéricos (Rango de edades)
    if edad_min:
        mascotas = mascotas.filter(edad_aproximada__gte=edad_min)  # gte = Mayor o igual que
    if edad_max:
        mascotas = mascotas.filter(edad_aproximada__lte=edad_max)  # lte = Menor o igual que

    # Filtros booleanos (Casillas de verificación)
    if vacunado:
        mascotas = mascotas.filter(vacunado=True)
    if esterilizado:
        mascotas = mascotas.filter(esterilizado=True)
    if microchip:
        mascotas = mascotas.filter(microchip=True)

    # 3. Enviamos todo al contexto para mantener los valores en el formulario HTML
    context = {
        'mascotas': mascotas,
        'busqueda': busqueda,
        'especie': especie,
        'sexo': sexo,
        'tamano': tamano,
        'raza': raza,
        'edadMin': edad_min,
        'edadMax': edad_max,
        'vacunado': vacunado,
        'esterilizado': esterilizado,
        'microchip': microchip,
    }
    return render(request, 'mascotas/lista.html', context)

from django.contrib import messages
# --- VISTA DE LISTA PARA EL ADMINISTRADOR ---
@roles_permitidos(['ADMIN', 'REFUGIO'])
def admin_lista_mascotas(request):
    if request.user.es_admin:
        # El administrador ve absolutamente todas las mascotas
        todas_las_mascotas = Mascota.objects.all().order_by('-fecha_registro')
    else:
        # CANDADO 1: El refugio ve SOLO las mascotas de su sede
        todas_las_mascotas = Mascota.objects.filter(refugio__usuario_encargado=request.user).order_by('-fecha_registro')

    return render(request, 'mascotas/admin_lista.html', {'mascotas': todas_las_mascotas})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def crear_mascota(request):
    refugios = Refugio.objects.filter(activo=True)
    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None

    if request.method == 'POST':
        try:  # <--- INICIA EL BLINDAJE
            mascota = Mascota()
            guardar_datos_mascota(request, mascota)

            if request.user.es_admin:
                refugio_id = request.POST.get('refugio')
                if refugio_id:
                    mascota.refugio_id = refugio_id
            else:
                mascota.refugio = mi_refugio

            mascota.save()
            messages.success(request, 'Mascota registrada correctamente.')
            return redirect('admin_lista_mascotas')

        except Exception as e:  # <--- SI ALGO FALLA, LO ATRAPAMOS AQUÍ
            messages.error(request, f'Error crítico al guardar la mascota: {str(e)}')
            # No hacemos redirect, dejamos que se vuelva a renderizar el formulario

    return render(request, 'mascotas/form.html', {'refugios': refugios, 'mi_refugio': mi_refugio})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    refugios = Refugio.objects.filter(activo=True)
    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None

    if not request.user.es_admin and mascota.refugio != mi_refugio:
        messages.error(request, 'Acceso Denegado: Esta mascota pertenece a otro refugio.')
        return redirect('admin_lista_mascotas')

    if request.method == 'POST':
        try:  # <--- INICIA EL BLINDAJE
            guardar_datos_mascota(request, mascota)

            if request.user.es_admin:
                refugio_id = request.POST.get('refugio')
                if refugio_id:
                    mascota.refugio_id = refugio_id
            else:
                mascota.refugio = mi_refugio

            mascota.save()
            messages.success(request, 'Mascota actualizada correctamente.')
            return redirect('admin_lista_mascotas')

        except Exception as e:  # <--- ATRAPAMOS EL ERROR
            messages.error(request, f'Error al intentar actualizar: {str(e)}')

    return render(request, 'mascotas/form.html', {'mascota': mascota, 'refugios': refugios, 'mi_refugio': mi_refugio})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None

    if not request.user.es_admin and mascota.refugio != mi_refugio:
        messages.error(request, 'Acceso Denegado: No puedes eliminar mascotas de otros refugios.')
        return redirect('admin_lista_mascotas')

    try:  # <--- INICIA EL BLINDAJE
        mascota.delete()
        messages.success(request, 'Mascota eliminada del sistema.')
    except Exception as e:  # <--- ATRAPAMOS EL ERROR (ej: base de datos bloqueada)
        messages.error(request,
                       f'No se pudo eliminar la mascota. Es posible que tenga adopciones vinculadas. Detalle: {str(e)}')

    return redirect('admin_lista_mascotas')


# --- FUNCIÓN AUXILIAR PARA GUARDAR DATOS (Se queda igual, EXCEPTO el refugio) ---
def guardar_datos_mascota(request, mascota):
    mascota.nombre = request.POST.get('nombre')
    mascota.especie = request.POST.get('especie')
    mascota.raza = request.POST.get('raza') or None
    mascota.fecha_nacimiento = request.POST.get('fechaNacimiento') or None
    mascota.sexo = request.POST.get('sexo')
    mascota.tamano = request.POST.get('tamano')
    mascota.peso = request.POST.get('peso') or None
    mascota.color = request.POST.get('color') or None
    mascota.descripcion = request.POST.get('descripcion') or None
    mascota.historial_medico = request.POST.get('historialMedico') or None
    mascota.fecha_ingreso = request.POST.get('fechaIngreso')
    mascota.estado_adopcion = request.POST.get('estadoAdopcion')

    if 'foto' in request.FILES:
        mascota.foto = request.FILES['foto']

    mascota.descripcion = request.POST.get('descripcion') or None

    if request.POST.get('fechaIngreso'):
        mascota.fecha_ingreso = request.POST.get('fechaIngreso')

    refugio_id = request.POST.get('refugio')
    if refugio_id:
        mascota.refugio = Refugio.objects.get(id_refugio=refugio_id)

    mascota.save()