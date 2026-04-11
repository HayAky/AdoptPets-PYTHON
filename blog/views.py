from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Blog, CategoriaBlog
from usuarios.decorators import roles_permitidos


# =========================================================
# VISTA PÚBLICA (Cualquier visitante)
# =========================================================
def lista_blogs(request):
    # Solo traemos los activos, ordenados del más reciente al más antiguo
    blogs = Blog.objects.filter(activo=True).order_by('-fecha_publicacion')
    return render(request, 'blog/lista.html', {'blogs': blogs})


# =========================================================
# PANEL DE GESTIÓN (Admins y Refugios)
# =========================================================
@roles_permitidos(['ADMIN', 'REFUGIO'])
def admin_lista_blogs(request):
    nombre_autor = f"{request.user.nombre} {request.user.apellido}"

    if request.user.es_admin:
        # El administrador ve TODO
        blogs = Blog.objects.all().order_by('-fecha_publicacion')
    else:
        # El refugio ve SOLO lo que él publicó (coincidencia de texto)
        blogs = Blog.objects.filter(autor=nombre_autor).order_by('-fecha_publicacion')

    return render(request, 'blog/admin_lista.html', {'blogs': blogs})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def crear_blog(request):
    categorias = CategoriaBlog.choices
    if request.method == 'POST':
        try:  # <-- BLINDAJE
            Blog.objects.create(
                titulo=request.POST.get('titulo'),
                resumen=request.POST.get('resumen'),
                contenido=request.POST.get('contenido'),
                categoria=request.POST.get('categoria') or None,
                imagen_url=request.POST.get('imagen_url'),
                autor=f"{request.user.nombre} {request.user.apellido}",
                fecha_publicacion=timezone.now().date(),
                activo=request.POST.get('activo') == 'on'
            )
            messages.success(request, 'Blog publicado exitosamente.')
            return redirect('admin_lista_blogs')
        except Exception as e:
            messages.error(request, f'Error al publicar el blog: {str(e)}')

    return render(request, 'blog/form.html', {'categorias': categorias})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def editar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id_blog=blog_id)
    categorias = CategoriaBlog.choices
    nombre_autor = f"{request.user.nombre} {request.user.apellido}"

    if not request.user.es_admin and blog.autor != nombre_autor:
        messages.error(request, 'No tienes permiso para editar esta publicación.')
        return redirect('admin_lista_blogs')

    if request.method == 'POST':
        try:  # <-- BLINDAJE
            blog.titulo = request.POST.get('titulo')
            blog.resumen = request.POST.get('resumen')
            blog.contenido = request.POST.get('contenido')
            blog.categoria = request.POST.get('categoria') or None
            blog.imagen_url = request.POST.get('imagen_url')
            blog.activo = request.POST.get('activo') == 'on'
            blog.save()
            messages.success(request, 'Blog actualizado correctamente.')
            return redirect('admin_lista_blogs')
        except Exception as e:
            messages.error(request, f'Error al guardar los cambios: {str(e)}')

    return render(request, 'blog/form.html', {'blog': blog, 'categorias': categorias})


@roles_permitidos(['ADMIN', 'REFUGIO'])
def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id_blog=blog_id)
    nombre_autor = f"{request.user.nombre} {request.user.apellido}"

    if not request.user.es_admin and blog.autor != nombre_autor:
        messages.error(request, 'No tienes permiso para eliminar esta publicación.')
        return redirect('admin_lista_blogs')

    try:  # <-- BLINDAJE
        blog.delete()
        messages.success(request, 'Blog eliminado.')
    except Exception as e:
        messages.error(request, 'Error al intentar eliminar la publicación.')

    return redirect('admin_lista_blogs')