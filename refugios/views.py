from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Refugio
from usuarios.decorators import roles_permitidos


# --- VISTA PÚBLICA ---
def lista_refugios(request):
    refugios = Refugio.objects.filter(activo=True)
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
    if request.method == 'POST':
        guardar_datos_refugio(request, Refugio())
        messages.success(request, 'Refugio creado correctamente.')
        return redirect('admin_lista_refugios')
    return render(request, 'refugios/form.html')


@roles_permitidos(['ADMIN'])
def editar_refugio(request, refugio_id):
    refugio = get_object_or_404(Refugio, id_refugio=refugio_id)
    if request.method == 'POST':
        guardar_datos_refugio(request, refugio)
        messages.success(request, 'Refugio actualizado correctamente.')
        return redirect('admin_lista_refugios')
    return render(request, 'refugios/form.html', {'refugio': refugio})


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
    # Si el checkbox viene en el POST es True (activo), si no, es False
    refugio.activo = request.POST.get('activo') == 'on'

    refugio.save()