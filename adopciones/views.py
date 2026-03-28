from django.shortcuts import render
from .models import Adopcion

def lista_adopciones(request):
    adopciones = Adopcion.objects.all()
    return render(request, 'adopciones/lista.html', {'adopciones': adopciones})