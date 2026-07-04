from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mascota
from refugios.models import Refugio
from blog.models import Blog
from django.db.models import Q
from usuarios.decorators import roles_permitidos
from usuarios.models import HistorialActividad
from .forms import MascotaForm

def inicio(request):
    # Usamos active_objects para que solo salgan las disponibles/activas en la home
    mascotas_destacadas = Mascota.active_objects.order_by('-fecha_registro')[:6]
    blogs_destacados = Blog.objects.filter(activo=True).order_by('-fecha_publicacion')[:2]

    return render(request, 'main.html', {
        'mascotas_destacadas': mascotas_destacadas, # Nombre consistente
        'blogs': blogs_destacados
    })
def lista_mascotas(request):
    mascotas = Mascota.objects.select_related('refugio').filter(estado_adopcion__in=['disponible', 'pendiente']).order_by('-fecha_registro')

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
        mascotas = mascotas.filter(raza__icontains=raza)

    if edad_min:
        mascotas = mascotas.filter(edad_aproximada__gte=edad_min)
    if edad_max:
        mascotas = mascotas.filter(edad_aproximada__lte=edad_max)

    if vacunado:
        mascotas = mascotas.filter(vacunado=True)
    if esterilizado:
        mascotas = mascotas.filter(esterilizado=True)
    if microchip:
        mascotas = mascotas.filter(microchip=True)

    busqueda = request.GET.get('busqueda', '')

    if busqueda and request.user.is_authenticated:
        HistorialActividad.objects.create(
            usuario=request.user,
            accion=f"Búsqueda: {busqueda}"
        )
    filtros = {
        'Busqueda': request.GET.get('busqueda', ''),
        'Especie': request.GET.get('especie', ''),
        'Sexo': request.GET.get('sexo', ''),
        'Tamaño': request.GET.get('tamano', ''),
        'Raza': request.GET.get('raza', ''),
        'Vacunado': 'Sí' if request.GET.get('vacunado') else '',
        'Esterilizado': 'Sí' if request.GET.get('esterilizado') else '',
        'Microchip': 'Sí' if request.GET.get('microchip') else '',
    }
    filtros_activos = [f"{k}: {v}" for k, v in filtros.items() if v]
    if filtros_activos and request.user.is_authenticated:
        accion_registrada = "Filtros aplicados: " + " | ".join(filtros_activos)

        ultima_accion = HistorialActividad.objects.filter(usuario=request.user).first()

        if not ultima_accion or ultima_accion.accion != accion_registrada:
            HistorialActividad.objects.create(
                usuario=request.user,
                accion=accion_registrada
            )


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
    # 1. Capturamos lo que el usuario escriba en el buscador
    busqueda = request.GET.get('busqueda', '')

    # 2. Base de datos según el rol
    if request.user.es_admin:
        mascotas = Mascota.objects.all().order_by('-fecha_registro')
    else:
        mascotas = Mascota.objects.filter(refugio__usuario_encargado=request.user).order_by('-fecha_registro')

    # 3. Si hay búsqueda, aplicamos el filtro múltiple
    if busqueda:
        mascotas = mascotas.filter(
            Q(nombre__icontains=busqueda) |
            Q(estado_adopcion__icontains=busqueda) |
            Q(especie__icontains=busqueda)
        )

    return render(request, 'mascotas/admin_lista.html', {
        'mascotas': mascotas,
        'busqueda': busqueda  # Lo enviamos para que la barra no se borre
    })

@roles_permitidos(['ADMIN', 'REFUGIO'])
def crear_mascota(request):
    refugios = Refugio.objects.filter(activo=True)
    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None

    if request.method == 'POST':
        try:
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

    if request.method == 'POST':
        # Instanciamos el formulario con los datos recibidos y la mascota actual
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()  # Guarda automáticamente
            messages.success(request, 'Mascota actualizada correctamente.')
            return redirect('admin_lista_mascotas')
        else:
            messages.error(request, 'Error al actualizar. Revisa los campos.')
    else:
        # Aquí inicializas el formulario para que se rellene con los datos actuales
        form = MascotaForm(instance=mascota)

    # AQUÍ ES DONDE ESTABA EL ERROR: Debes enviar 'form' al contexto
    return render(request, 'mascotas/form.html', {
        'form': form,
        'mascota': mascota
    })

@roles_permitidos(['ADMIN', 'REFUGIO'])
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)

    # Blindaje de seguridad (si no es admin y no es su refugio)
    if not request.user.es_admin and mascota.refugio != getattr(request.user, 'mi_refugio', None):
        messages.error(request, 'Acceso Denegado.')
        return redirect('admin_lista_mascotas')

    # CAMBIO: Aquí ya no se hace .delete()
    mascota.activo = False
    mascota.save()

    messages.success(request, 'Mascota marcada como Adoptada/Inactiva.')
    return redirect('admin_lista_mascotas')


@roles_permitidos(['ADMIN', 'REFUGIO'])
def reactivar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)

    # Simplemente volvemos a poner activo en True
    mascota.activo = True
    mascota.save()

    messages.success(request, 'Mascota reactivada correctamente.')
    return redirect('admin_lista_mascotas')


def guardar_datos_mascota(request, mascota):
    # 1. Campos de texto básicos que ya coincidían
    mascota.nombre = request.POST.get('nombre')
    mascota.especie = request.POST.get('especie')
    mascota.raza = request.POST.get('raza') or None
    mascota.sexo = request.POST.get('sexo')
    mascota.tamano = request.POST.get('tamano')
    mascota.peso = request.POST.get('peso') or None
    mascota.color = request.POST.get('color') or None
    mascota.descripcion = request.POST.get('descripcion') or None

    # 2. CORREGIDO: Emparejamos 'edadAproximada' del HTML con el modelo
    edad_aprox = request.POST.get('edadAproximada')
    mascota.edad_aproximada = edad_aprox if edad_aprox else None

    # 3. CORREGIDO: Emparejamos 'estadoSalud' del HTML con el modelo
    mascota.estado_salud = request.POST.get('estadoSalud') or None

    # 4. NUEVO: Ahora sí guardamos los checkboxes médicos
    mascota.vacunado = request.POST.get('vacunado') == 'on'
    mascota.esterilizado = request.POST.get('esterilizado') == 'on'
    mascota.microchip = request.POST.get('microchip') == 'on'

    # 5. Estado y Fechas
    mascota.estado_adopcion = request.POST.get('estadoAdopcion')

    fecha_ingreso = request.POST.get('fechaIngreso')
    if fecha_ingreso:
        mascota.fecha_ingreso = fecha_ingreso

    # 6. Guardar la fotografía si el usuario subió una nueva
    if 'foto' in request.FILES:
        mascota.foto = request.FILES['foto']


def detalle_mascota(request, mascota_id):
    # Trae la mascota, su refugio y sus fotos asociadas
    mascota = get_object_or_404(
        Mascota.objects.select_related('refugio').prefetch_related('fotos'),
        id_mascota=mascota_id
    )

    return render(request, 'mascotas/detalle.html', {'mascota': mascota})