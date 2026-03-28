from django.shortcuts import render
from .models import Blog

def lista_blogs(request):
    blogs = Blog.objects.filter(activo=True) # Solo traemos los activos
    return render(request, 'blog/lista.html', {'blogs': blogs})