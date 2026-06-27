from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from refugios.models import Refugio
from blog.models import Blog
from django.db.models import Q
from usuarios.decorators import roles_permitidos
from .forms import MascotaForm
from mascotas.models import Mascota


# mascotas/views.py
def inicio(request):
    mascotas = Mascota.objects.all() # Verifica que existan registros
    return render(request, 'main.html', {'mascotas': mascotas})
def lista_mascotas(request):
    mascotas = Mascota.objects.filter(estado_adopcion='disponible').order_by('-fecha_registro')

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
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)

            # Asignación de refugio
            if request.user.es_admin:
                mascota.refugio_id = request.POST.get('refugio')
            else:
                mascota.refugio = mi_refugio

            mascota.save()  # Aquí Cloudinary sube la foto
            messages.success(request, 'Mascota registrada correctamente.')
            return redirect('admin_lista_mascotas')
    else:
        form = MascotaForm()

    return render(request, 'mascotas/form.html', {
        'form': form,
        'refugios': refugios,
        'mi_refugio': mi_refugio
    })


@roles_permitidos(['ADMIN', 'REFUGIO'])
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    refugios = Refugio.objects.filter(activo=True)
    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None

    # Mantenemos tu seguridad de refugios
    if not request.user.es_admin and mascota.refugio != mi_refugio:
        messages.error(request, 'Acceso Denegado: Esta mascota pertenece a otro refugio.')
        return redirect('admin_lista_mascotas')

    if request.method == 'POST':
        # Usamos el form para procesar los datos (incluyendo la foto automáticamente)
        form = MascotaForm(request.POST, request.FILES, instance=mascota)

        if form.is_valid():
            try:
                # Guardamos los datos del formulario (esto incluye la foto en Cloudinary)
                mascota_actualizada = form.save(commit=False)

                # Mantenemos tu lógica de asignación de refugio
                if request.user.es_admin:
                    refugio_id = request.POST.get('refugio')
                    if refugio_id:
                        mascota_actualizada.refugio_id = refugio_id
                else:
                    mascota_actualizada.refugio = mi_refugio

                mascota_actualizada.save()
                messages.success(request, 'Mascota actualizada correctamente.')
                return redirect('admin_lista_mascotas')

            except Exception as e:
                messages.error(request, f'Error al intentar actualizar: {str(e)}')
        else:
            messages.error(request, 'Error en el formulario. Revisa los datos.')
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'mascotas/form.html', {
        'form': form,  # Pasamos el formulario
        'mascota': mascota,
        'refugios': refugios,
        'mi_refugio': mi_refugio
    })


@roles_permitidos(['ADMIN', 'REFUGIO'])
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    mi_refugio = getattr(request.user, 'mi_refugio', None) if not request.user.es_admin else None

    if not request.user.es_admin and mascota.refugio != mi_refugio:
        messages.error(request, 'Acceso Denegado: No puedes eliminar mascotas de otros refugios.')
        return redirect('admin_lista_mascotas')

    try:
        mascota.delete()
        messages.success(request, 'Mascota eliminada del sistema.')
    except Exception as e:
        messages.error(request,
                       f'No se pudo eliminar la mascota. Es posible que tenga adopciones vinculadas. Detalle: {str(e)}')

    return redirect('admin_lista_mascotas')

# mascotas/views.py

def inicio(request):
    mascotas = Mascota.objects.order_by('-fecha_registro')[:6]
    mascotas_procesadas = []

    for m in mascotas:
        mascotas_procesadas.append({
            'nombre': m.nombre,
            'especie': m.especie,
            'edad_aproximada': m.edad_aproximada,
            # Extraemos la URL como string plano aquí
            'foto_url': m.foto.url if m.foto else None
        })

    return render(request, 'main.html', {'mascotas_destacadas': mascotas_procesadas})