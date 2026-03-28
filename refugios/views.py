from django.shortcuts import render
from .models import Refugio

def lista_refugios(request):
    refugios = Refugio.objects.all()
    return render(request, 'refugios/lista.html', {'refugios': refugios})