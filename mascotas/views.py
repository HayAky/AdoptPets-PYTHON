from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mascota
from refugios.models import Refugio


from usuarios.decorators import roles_permitidos
def lista_mascotas(request):
    # Traemos todas las mascotas (o puedes usar .filter() para traer solo las disponibles)
    todas_las_mascotas = Mascota.objects.all()
    return render(request, 'mascotas/lista.html', {'mascotas': todas_las_mascotas})

from django.contrib import messages
# --- VISTA DE LISTA PARA EL ADMINISTRADOR ---
@roles_permitidos(['ADMIN', 'REFUGIO'])
def admin_lista_mascotas(request):
    todas_las_mascotas = Mascota.objects.all().order_by('-fecha_registro')
    return render(request, 'mascotas/admin_lista.html', {'mascotas': todas_las_mascotas})

# --- 1. VISTA PARA CREAR MASCOTA ---
@roles_permitidos(['ADMIN', 'REFUGIO'])
def crear_mascota(request):
    refugios = Refugio.objects.filter(activo=True)
    if request.method == 'POST':
        guardar_datos_mascota(request, Mascota())
        messages.success(request, 'Mascota creada correctamente.')
        return redirect('admin_lista_mascotas')
    return render(request, 'mascotas/form.html', {'refugios': refugios})

@roles_permitidos(['ADMIN', 'REFUGIO'])
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    refugios = Refugio.objects.filter(activo=True)
    if request.method == 'POST':
        guardar_datos_mascota(request, mascota)
        messages.success(request, 'Mascota actualizada correctamente.')
        return redirect('admin_lista_mascotas')
    return render(request, 'mascotas/form.html', {'mascota': mascota, 'refugios': refugios})

@roles_permitidos(['ADMIN', 'REFUGIO'])
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    mascota.delete()
    messages.success(request, 'Mascota eliminada correctamente.')
    return redirect('admin_lista_mascotas')


# --- FUNCIÓN AUXILIAR PARA GUARDAR DATOS ---
def guardar_datos_mascota(request, mascota):
    mascota.nombre = request.POST.get('nombre')
    mascota.especie = request.POST.get('especie')
    mascota.raza = request.POST.get('raza')
    mascota.edad_aproximada = request.POST.get('edadAproximada') or None
    mascota.sexo = request.POST.get('sexo')
    mascota.tamano = request.POST.get('tamano')
    mascota.peso = request.POST.get('peso') or None
    mascota.color = request.POST.get('color')
    mascota.descripcion = request.POST.get('descripcion')
    mascota.estado_salud = request.POST.get('estadoSalud')

    mascota.vacunado = request.POST.get('vacunado') == 'on'
    mascota.esterilizado = request.POST.get('esterilizado') == 'on'
    mascota.microchip = request.POST.get('microchip') == 'on'
    mascota.estado_adopcion = request.POST.get('estadoAdopcion', 'disponible')

    if request.POST.get('fechaIngreso'):
        mascota.fecha_ingreso = request.POST.get('fechaIngreso')

    refugio_id = request.POST.get('refugio')
    if refugio_id:
        mascota.refugio = Refugio.objects.get(id_refugio=refugio_id)

    mascota.save()