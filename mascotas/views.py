from django.shortcuts import render
from .models import Mascota


def lista_mascotas(request):
    # Esto es el equivalente exacto a: mascotaRepository.findAll()
    todas_las_mascotas = Mascota.objects.all()

    # Pasamos los datos al HTML mediante un diccionario de contexto
    contexto = {
        'mascotas': todas_las_mascotas
    }
    return render(request, 'mascotas/lista.html', contexto)
