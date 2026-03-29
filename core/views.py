from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from datetime import date, datetime

from .models import (
    Usuario, Rol, Refugio, Mascota, GaleriaFoto,
    Adopcion, Seguimiento, Noticia, Blog, Comentario,
    EstadoAdopcion, CategoriaBlog, CategoriaNoticia
)


# ─── DECORADOR DE ROL ────────────────────────────────────────────────────────

def rol_requerido(*roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            tiene_permiso = False
            for rol in roles:
                nombre = f'ROLE_{rol}' if not rol.startswith('ROLE_') else rol
                if request.user.tiene_rol(nombre):
                    tiene_permiso = True
                    break
            if not tiene_permiso:
                return redirect('error403')
            return view_func(request, *args, **kwargs)
        wrapper.__name__ = view_func.__name__
        return wrapper
    return decorator


# ─── PÚBLICO ─────────────────────────────────────────────────────────────────

def raiz(request):
    return redirect('main')

def main(request):
    # Traemos las mascotas que tengan estado 'Disponible'
    ultimas_mascotas = Mascota.objects.filter(
        estado_adopcion=EstadoAdopcion.DISPONIBLE
    ).order_by('-id_mascota')[:3] # Trae las 3 más recientes
    
    count = Mascota.objects.filter(estado_adopcion=EstadoAdopcion.DISPONIBLE).count()
    
    # IMPORTANTE: El nombre 'ultimas_mascotas' debe coincidir con el del HTML
    return render(request, 'main.html', {
        'mascotasDisponibles': count,
        'ultimas_mascotas': ultimas_mascotas
    })    
def adoptar(request):
    qs = Mascota.objects.filter(estado_adopcion=EstadoAdopcion.DISPONIBLE).select_related('refugio')
    especie      = request.GET.get('especie', '')
    sexo         = request.GET.get('sexo', '')
    tamano       = request.GET.get('tamano', '')
    raza         = request.GET.get('raza', '')
    edad_min     = request.GET.get('edadMin', '')
    edad_max     = request.GET.get('edadMax', '')
    vacunado     = request.GET.get('vacunado', '')
    esterilizado = request.GET.get('esterilizado', '')
    microchip    = request.GET.get('microchip', '')
    refugio_id   = request.GET.get('refugioId', '')
    busqueda     = request.GET.get('busqueda', '')

    if busqueda:
        qs = qs.filter(Q(nombre__icontains=busqueda)|Q(especie__icontains=busqueda)|Q(raza__icontains=busqueda))
    if especie:
        qs = qs.filter(especie__iexact=especie)
    if sexo:
        qs = qs.filter(sexo__iexact=sexo)
    if tamano:
        qs = qs.filter(tamano__iexact=tamano)
    if raza:
        qs = qs.filter(raza__icontains=raza)
    if edad_min:
        qs = qs.filter(edad_aproximada__gte=int(edad_min))
    if edad_max:
        qs = qs.filter(edad_aproximada__lte=int(edad_max))
    if vacunado:
        qs = qs.filter(vacunado=True)
    if esterilizado:
        qs = qs.filter(esterilizado=True)
    if microchip:
        qs = qs.filter(microchip=True)
    if refugio_id:
        qs = qs.filter(refugio_id=refugio_id)

    return render(request, 'mascotas.html', {
        'mascotas': qs, 'refugios': Refugio.objects.all(),
        'especie': especie, 'sexo': sexo, 'tamano': tamano,
        'raza': raza, 'busqueda': busqueda,
    })

def refugios_publicos(request):
    return render(request, 'refugios.html', {'refugios': Refugio.objects.all()})

def contacto(request):
    return render(request, 'contacto.html')

def contactenos(request):
    return render(request, 'contactenos.html')

def error404(request):
    return render(request, 'error404.html')

def error403(request):
    return render(request, 'error403.html')


# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if user.tiene_rol('ROLE_ADMIN'):
                return redirect('admin_dashboard')
            elif user.tiene_rol('ROLE_REFUGIO'):
                return redirect('refugio_dashboard')
            else:
                return redirect('adoptante_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    tipo = request.GET.get('tipo', 'adoptante')
    if request.method == 'POST':
        nombre           = request.POST.get('nombre', '')
        apellido         = request.POST.get('apellido', '')
        email            = request.POST.get('email', '')
        password         = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        tipo_registro    = request.POST.get('tipoRegistro', 'adoptante')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'register.html', {'tipo': tipo_registro})
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'register.html', {'tipo': tipo_registro})
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return render(request, 'register.html', {'tipo': tipo_registro})

        nombre_rol = 'ROLE_REFUGIO' if tipo_registro == 'refugio' else 'ROLE_ADOPTANTE'
        try:
            rol = Rol.objects.get(nombre_rol=nombre_rol)
        except Rol.DoesNotExist:
            messages.error(request, 'Error de configuración. Contacta al administrador.')
            return render(request, 'register.html', {'tipo': tipo_registro})

        usuario = Usuario.objects.create_user(
            email=email, password=password,
            nombre=nombre, apellido=apellido, activo=True, ciudad='Bogotá'
        )
        usuario.roles.add(rol)
        messages.success(request, 'Registro exitoso. Ya puedes iniciar sesión')
        return redirect('login')
    return render(request, 'register.html', {'tipo': tipo})

@login_required
def perfil(request):
    user = request.user
    if user.tiene_rol('ROLE_ADMIN'):
        return redirect('admin_dashboard')
    elif user.tiene_rol('ROLE_REFUGIO'):
        return redirect('refugio_dashboard')
    else:
        return redirect('adoptante_perfil')

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        password_actual = request.POST.get('passwordActual')
        password_nueva  = request.POST.get('passwordNueva')
        confirm         = request.POST.get('confirmPassword')
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('cambiar_password')
        if password_nueva != confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('cambiar_password')
        if len(password_nueva) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return redirect('cambiar_password')
        request.user.set_password(password_nueva)
        request.user.save()
        messages.success(request, 'Contraseña actualizada exitosamente')
        return redirect('perfil')
    return render(request, 'cambiar-password.html', {'usuario': request.user})


# ─── BLOG ────────────────────────────────────────────────────────────────────

def blog_lista(request):
    posts = Blog.objects.all().order_by('-fecha_publicacion')
    return render(request, 'blog/lista.html', {'posts': posts, 'categorias': CategoriaBlog.choices})

def blog_detalle(request, id):
    post = get_object_or_404(Blog, pk=id)
    Blog.objects.filter(pk=id).update(visitas=post.visitas + 1)
    return render(request, 'blog/detalle.html', {'post': post})


# ─── NOTICIAS ────────────────────────────────────────────────────────────────

def noticias_lista(request):
    noticias = Noticia.objects.all().order_by('-fecha_publicacion')
    return render(request, 'noticias/lista.html', {'noticias': noticias, 'categorias': CategoriaNoticia.choices})

def noticia_detalle(request, id):
    noticia = get_object_or_404(Noticia, pk=id)
    return render(request, 'noticias/detalle.html', {'noticia': noticia})

def noticias_categoria(request, categoria):
    noticias = Noticia.objects.filter(categoria=categoria)
    return render(request, 'noticias/lista.html', {
        'noticias': noticias, 'categoriaActual': categoria, 'categorias': CategoriaNoticia.choices
    })


# ─── ADOPTANTE ───────────────────────────────────────────────────────────────

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_dashboard(request):
    adopciones = Adopcion.objects.filter(adoptante=request.user).select_related('mascota')
    return render(request, 'adoptante/dashboard.html', {
        'usuario': request.user,
        'misAdopciones': adopciones,
        'solicitudesPendientes': adopciones.filter(estado_adopcion=EstadoAdopcion.PENDIENTE).count(),
        'solicitudesAprobadas':  adopciones.filter(estado_adopcion=EstadoAdopcion.APROBADA).count(),
        'adopcionesCompletadas': adopciones.filter(estado_adopcion=EstadoAdopcion.COMPLETADA).count(),
    })

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_mascotas(request):
    qs       = Mascota.objects.filter(estado_adopcion=EstadoAdopcion.DISPONIBLE)
    busqueda = request.GET.get('busqueda', '')
    especie  = request.GET.get('especie', '')
    sexo     = request.GET.get('sexo', '')
    if busqueda:
        qs = qs.filter(Q(nombre__icontains=busqueda)|Q(especie__icontains=busqueda)|Q(raza__icontains=busqueda))
    elif especie:
        qs = qs.filter(especie__iexact=especie)
    if sexo:
        qs = qs.filter(sexo__iexact=sexo)
    return render(request, 'adoptante/mascotas.html', {
        'mascotas': qs, 'busqueda': busqueda, 'especie': especie, 'sexo': sexo
    })

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_mascota_detalle(request, id):
    mascota = get_object_or_404(Mascota, pk=id)
    return render(request, 'adoptante/mascota-detalle.html', {'mascota': mascota})

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_mis_adopciones(request):
    adopciones = Adopcion.objects.filter(adoptante=request.user).select_related('mascota')
    return render(request, 'adoptante/mis-adopciones.html', {'adopciones': adopciones})

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_adopcion_detalle(request, id):
    adopcion = get_object_or_404(Adopcion, pk=id)
    if adopcion.adoptante != request.user and not request.user.tiene_rol('ROLE_ADMIN'):
        return redirect('error403')
    return render(request, 'adoptante/adopcion-detalle.html', {'adopcion': adopcion})

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_solicitar(request, mascota_id):
    if request.method == 'POST':
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        if mascota.estado_adopcion != EstadoAdopcion.DISPONIBLE:
            messages.error(request, 'La mascota ya no está disponible')
            return redirect('adoptante_mascotas')
        Adopcion.objects.create(
            adoptante=request.user, mascota=mascota,
            fecha_solicitud=date.today(),
            estado_adopcion=EstadoAdopcion.PENDIENTE,
            observaciones=request.POST.get('observaciones', '')
        )
        mascota.estado_adopcion = EstadoAdopcion.EN_PROCESO
        mascota.save()
        messages.success(request, 'Solicitud enviada exitosamente')
        return redirect('adoptante_mis_adopciones')
    return redirect('adoptante_mascotas')

@login_required
@rol_requerido('ADOPTANTE', 'ADMIN')
def adoptante_perfil(request):
    if request.method == 'POST':
        u = request.user
        u.nombre    = request.POST.get('nombre', u.nombre)
        u.apellido  = request.POST.get('apellido', u.apellido)
        u.telefono  = request.POST.get('telefono', u.telefono)
        u.direccion = request.POST.get('direccion', u.direccion)
        u.ciudad    = request.POST.get('ciudad', u.ciudad)
        u.save()
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('adoptante_perfil')
    return render(request, 'adoptante/perfil.html', {'usuario': request.user})


# ─── REFUGIO ─────────────────────────────────────────────────────────────────

def _get_refugio_usuario(usuario):
    return Refugio.objects.filter(email=usuario.email).first()

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_dashboard(request):
    refugio = _get_refugio_usuario(request.user)
    ctx = {'usuario': request.user, 'refugio': refugio}
    if refugio:
        adopciones = Adopcion.objects.filter(mascota__refugio=refugio)
        ctx.update({
            'totalMascotas':         Mascota.objects.filter(refugio=refugio).count(),
            'mascotasDisponibles':   Mascota.objects.filter(refugio=refugio, estado_adopcion=EstadoAdopcion.DISPONIBLE).count(),
            'solicitudesPendientes': adopciones.filter(estado_adopcion=EstadoAdopcion.PENDIENTE).count(),
            'adopcionesCompletadas': adopciones.filter(estado_adopcion=EstadoAdopcion.COMPLETADA).count(),
            'ultimasMascotas':       Mascota.objects.filter(refugio=refugio).order_by('-fecha_registro')[:5],
            'adopcionesPendientes':  adopciones.filter(estado_adopcion=EstadoAdopcion.PENDIENTE).select_related('adoptante','mascota')[:5],
        })
    else:
        ctx['sinRefugio'] = True
    return render(request, 'refugio/dashboard.html', ctx)

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_mascotas(request):
    refugio  = get_object_or_404(Refugio, email=request.user.email)
    mascotas = Mascota.objects.filter(refugio=refugio)
    return render(request, 'refugio/mascotas/lista.html', {'mascotas': mascotas, 'refugio': refugio})

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_mascota_form(request, id=None):
    refugio = get_object_or_404(Refugio, email=request.user.email)
    mascota = get_object_or_404(Mascota, pk=id) if id else None
    if request.method == 'POST':
        data = request.POST
        if mascota is None:
            mascota = Mascota()
        mascota.nombre          = data.get('nombre')
        mascota.especie         = data.get('especie')
        mascota.raza            = data.get('raza', '')
        mascota.edad_aproximada = data.get('edadAproximada') or None
        mascota.sexo            = data.get('sexo')
        mascota.tamano          = data.get('tamano')
        mascota.descripcion     = data.get('descripcion', '')
        mascota.vacunado        = 'vacunado' in data
        mascota.esterilizado    = 'esterilizado' in data
        mascota.microchip       = 'microchip' in data
        mascota.estado_adopcion = data.get('estadoAdopcion', EstadoAdopcion.DISPONIBLE)
        mascota.refugio         = refugio
        # Foto principal
        if 'foto_principal' in request.FILES:
            mascota.foto_principal = request.FILES['foto_principal']
        mascota.save()
        # Galería
        for foto_file in request.FILES.getlist('galeria_fotos'):
            GaleriaFoto.objects.create(mascota=mascota, foto=foto_file)
        messages.success(request, 'Mascota guardada exitosamente')
        return redirect('refugio_mascotas')
    return render(request, 'refugio/mascotas/form.html', {'mascota': mascota, 'refugio': refugio})

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_mascota_eliminar(request, id):
    refugio = get_object_or_404(Refugio, email=request.user.email)
    mascota = get_object_or_404(Mascota, pk=id)
    if mascota.refugio != refugio:
        return redirect('error403')
    try:
        mascota.delete()
        messages.success(request, 'Mascota eliminada')
    except Exception as e:
        messages.error(request, f'No se puede eliminar: {e}')
    return redirect('refugio_mascotas')

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_adopciones(request):
    refugio    = get_object_or_404(Refugio, email=request.user.email)
    adopciones = Adopcion.objects.filter(mascota__refugio=refugio).select_related('adoptante','mascota')
    estado     = request.GET.get('estado', '')
    if estado:
        adopciones = adopciones.filter(estado_adopcion=estado)
    return render(request, 'refugio/adopciones/lista.html', {
        'adopciones': adopciones, 'refugio': refugio, 'estadoFiltro': estado
    })

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_adopcion_detalle(request, id):
    refugio  = get_object_or_404(Refugio, email=request.user.email)
    adopcion = get_object_or_404(Adopcion, pk=id)
    if adopcion.mascota.refugio != refugio:
        return redirect('error403')
    return render(request, 'refugio/adopciones/detalle.html', {'adopcion': adopcion})

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_aprobar_adopcion(request, id):
    if request.method == 'POST':
        adopcion = get_object_or_404(Adopcion, pk=id)
        adopcion.estado_adopcion  = EstadoAdopcion.APROBADA
        adopcion.fecha_aprobacion = date.today()
        adopcion.save()
        messages.success(request, 'Adopción aprobada')
    return redirect('refugio_adopciones')

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_rechazar_adopcion(request, id):
    if request.method == 'POST':
        adopcion = get_object_or_404(Adopcion, pk=id)
        motivo   = request.POST.get('motivo', '')
        adopcion.estado_adopcion         = EstadoAdopcion.RECHAZADA
        adopcion.observaciones           = (adopcion.observaciones or '') + f'\nMotivo: {motivo}'
        adopcion.mascota.estado_adopcion = EstadoAdopcion.DISPONIBLE
        adopcion.mascota.save()
        adopcion.save()
        messages.success(request, 'Adopción rechazada')
    return redirect('refugio_adopciones')

@login_required
@rol_requerido('REFUGIO', 'ADMIN')
def refugio_perfil(request):
    refugio = Refugio.objects.filter(email=request.user.email).first() or Refugio()
    if request.method == 'POST':
        data = request.POST
        refugio.nombre_refugio   = data.get('nombreRefugio', '')
        refugio.direccion        = data.get('direccion', '')
        refugio.telefono         = data.get('telefono', '')
        refugio.localidad        = data.get('localidad', '')
        refugio.capacidad_maxima = data.get('capacidadMaxima') or None
        refugio.descripcion      = data.get('descripcion', '')
        refugio.email            = request.user.email
        refugio.activo           = True
        # Foto del refugio
        if 'foto' in request.FILES:
            refugio.foto = request.FILES['foto']
        refugio.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('refugio_perfil')
    return render(request, 'refugio/perfil.html', {'usuario': request.user, 'refugio': refugio})


# ─── ADMIN ───────────────────────────────────────────────────────────────────

@login_required
@rol_requerido('ADMIN')
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html', {
        'totalMascotas':         Mascota.objects.count(),
        'mascotasDisponibles':   Mascota.objects.filter(estado_adopcion=EstadoAdopcion.DISPONIBLE).count(),
        'solicitudesPendientes': Adopcion.objects.filter(estado_adopcion=EstadoAdopcion.PENDIENTE).count(),
        'adopcionesCompletadas': Adopcion.objects.filter(estado_adopcion=EstadoAdopcion.COMPLETADA).count(),
        'totalUsuarios':         Usuario.objects.count(),
        'totalRefugios':         Refugio.objects.count(),
        'adopcionesPendientes':  Adopcion.objects.filter(estado_adopcion=EstadoAdopcion.PENDIENTE).select_related('adoptante','mascota')[:10],
        'ultimasMascotas':       Mascota.objects.filter(estado_adopcion=EstadoAdopcion.DISPONIBLE).order_by('-fecha_registro')[:5],
    })

@login_required
@rol_requerido('ADMIN')
def admin_mascotas(request):
    refugio_id = request.GET.get('refugio')
    mascotas   = Mascota.objects.filter(refugio_id=refugio_id).select_related('refugio') if refugio_id else Mascota.objects.all().select_related('refugio')
    return render(request, 'admin/mascotas/lista.html', {'mascotas': mascotas})


# ── ADMIN: FORMULARIO MASCOTA (crear / editar) con fotos ─────────────────────
@login_required
@rol_requerido('ADMIN')
def admin_mascota_form(request, id=None):
    mascota  = get_object_or_404(Mascota, id_mascota=id) if id else None
    refugios = Refugio.objects.all()

    if request.method == 'POST':
        nombre          = request.POST.get('nombre', '').strip()
        especie         = request.POST.get('especie', '')
        raza            = request.POST.get('raza', '').strip()
        edad            = request.POST.get('edad_aproximada') or None
        sexo            = request.POST.get('sexo', '')
        tamano          = request.POST.get('tamano', '')
        peso            = request.POST.get('peso') or None
        color           = request.POST.get('color', '').strip()
        descripcion     = request.POST.get('descripcion', '').strip()
        estado_salud    = request.POST.get('estado_salud', '').strip()
        estado_adopcion = request.POST.get('estado_adopcion', 'disponible')
        refugio_id      = request.POST.get('refugio') or None

        vacunado      = 'vacunado'      in request.POST
        esterilizado  = 'esterilizado'  in request.POST
        desparasitado = 'desparasitado' in request.POST
        apto_ninos    = 'apto_ninos'    in request.POST
        apto_mascotas = 'apto_mascotas' in request.POST

        if not nombre or not especie or not sexo:
            messages.error(request, 'Nombre, especie y sexo son obligatorios.')
        else:
            if mascota is None:
                mascota = Mascota()

            mascota.nombre          = nombre
            mascota.especie         = especie
            mascota.raza            = raza
            mascota.edad_aproximada = edad
            mascota.sexo            = sexo
            mascota.tamano          = tamano
            mascota.peso            = peso
            mascota.color           = color
            mascota.descripcion     = descripcion
            mascota.estado_salud    = estado_salud
            mascota.estado_adopcion = estado_adopcion
            mascota.vacunado        = vacunado
            mascota.esterilizado    = esterilizado
            mascota.apto_ninos      = apto_ninos
            mascota.apto_mascotas   = apto_mascotas

            if refugio_id:
                try:
                    mascota.refugio = Refugio.objects.get(id_refugio=refugio_id)
                except Refugio.DoesNotExist:
                    pass

            # Foto principal
            if 'foto_principal' in request.FILES:
                mascota.foto_principal = request.FILES['foto_principal']

            mascota.save()

            # Galería de fotos
            for foto_file in request.FILES.getlist('galeria_fotos'):
                GaleriaFoto.objects.create(mascota=mascota, foto=foto_file)

            messages.success(request, f'Mascota "{mascota.nombre}" guardada correctamente.')
            return redirect('admin_mascotas')

    return render(request, 'admin/mascotas/form.html', {
        'mascota': mascota,
        'refugios': refugios,
    })


# ── ADMIN: ELIMINAR MASCOTA ───────────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN')
def admin_mascota_eliminar(request, id):
    mascota = get_object_or_404(Mascota, pk=id)
    try:
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'Mascota "{nombre}" eliminada.')
    except Exception:
        messages.error(request, 'No se puede eliminar. Tiene adopciones asociadas.')
    return redirect('admin_mascotas')


@login_required
@rol_requerido('ADMIN')
def admin_adopciones(request):
    adopciones = Adopcion.objects.all().select_related('adoptante','mascota','mascota__refugio')
    return render(request, 'admin/adopciones/lista.html', {'adopciones': adopciones})

@login_required
@rol_requerido('ADMIN')
def admin_adopciones_pendientes(request):
    adopciones = Adopcion.objects.filter(estado_adopcion=EstadoAdopcion.PENDIENTE).select_related('adoptante','mascota')
    return render(request, 'admin/adopciones/pendientes.html', {'adopciones': adopciones})

@login_required
@rol_requerido('ADMIN')
def admin_adopcion_detalle(request, id):
    adopcion = get_object_or_404(Adopcion, pk=id)
    return render(request, 'admin/adopciones/detalle.html', {'adopcion': adopcion})

@login_required
@rol_requerido('ADMIN')
def admin_aprobar_adopcion(request, id):
    if request.method == 'POST':
        adopcion = get_object_or_404(Adopcion, pk=id)
        adopcion.estado_adopcion  = EstadoAdopcion.APROBADA
        adopcion.fecha_aprobacion = date.today()
        adopcion.save()
        messages.success(request, 'Adopción aprobada')
    return redirect('admin_adopciones_pendientes')

@login_required
@rol_requerido('ADMIN')
def admin_rechazar_adopcion(request, id):
    if request.method == 'POST':
        adopcion = get_object_or_404(Adopcion, pk=id)
        motivo   = request.POST.get('motivo', '')
        adopcion.estado_adopcion         = EstadoAdopcion.RECHAZADA
        adopcion.observaciones           = (adopcion.observaciones or '') + f'\nMotivo: {motivo}'
        adopcion.mascota.estado_adopcion = EstadoAdopcion.DISPONIBLE
        adopcion.mascota.save()
        adopcion.save()
        messages.success(request, 'Adopción rechazada')
    return redirect('admin_adopciones_pendientes')

@login_required
@rol_requerido('ADMIN')
def admin_completar_adopcion(request, id):
    if request.method == 'POST':
        adopcion = get_object_or_404(Adopcion, pk=id)
        adopcion.estado_adopcion         = EstadoAdopcion.COMPLETADA
        adopcion.mascota.estado_adopcion = 'adoptada'
        adopcion.mascota.save()
        adopcion.save()
        messages.success(request, 'Adopción completada')
    return redirect('admin_adopciones')

@login_required
@rol_requerido('ADMIN')
def admin_usuarios(request):
    usuarios = Usuario.objects.prefetch_related('roles').all()
    return render(request, 'admin/usuarios/lista.html', {
        'usuarios':           usuarios,
        'cantidadActivos':    usuarios.filter(activo=True).count(),
        'cantidadAdoptantes': sum(1 for u in usuarios if u.tiene_rol('ROLE_ADOPTANTE')),
        'cantidadRefugios':   sum(1 for u in usuarios if u.tiene_rol('ROLE_REFUGIO')),
    })

@login_required
@rol_requerido('ADMIN')
def admin_usuario_editar(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if request.method == 'POST':
        data = request.POST
        usuario.nombre    = data.get('nombre', usuario.nombre)
        usuario.apellido  = data.get('apellido', usuario.apellido)
        usuario.telefono  = data.get('telefono', usuario.telefono)
        usuario.direccion = data.get('direccion', usuario.direccion)
        usuario.ciudad    = data.get('ciudad', usuario.ciudad)
        usuario.cedula    = data.get('cedula', usuario.cedula)
        usuario.activo    = 'activo' in data
        usuario.save()
        messages.success(request, 'Usuario actualizado')
        return redirect('admin_usuarios')
    return render(request, 'admin/usuarios/form.html', {'usuario': usuario})

@login_required
@rol_requerido('ADMIN')
def admin_usuario_toggle(request, id):
    if request.method == 'POST':
        usuario        = get_object_or_404(Usuario, pk=id)
        usuario.activo = not usuario.activo
        usuario.save()
        messages.success(request, f'Usuario {"activado" if usuario.activo else "desactivado"}')
    return redirect('admin_usuarios')

@login_required
@rol_requerido('ADMIN')
def admin_usuario_resetear_password(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    usuario.set_password('123456')
    usuario.save()
    messages.success(request, 'Contraseña reseteada a: 123456')
    return redirect('admin_usuarios')

@login_required
@rol_requerido('ADMIN')
def admin_refugios(request):
    return render(request, 'admin/refugios/lista.html', {'refugios': Refugio.objects.all()})


# ── ADMIN: FORMULARIO REFUGIO (crear / editar) con foto ──────────────────────
@login_required
@rol_requerido('ADMIN')
def admin_refugio_form(request, id=None):
    refugio = get_object_or_404(Refugio, id_refugio=id) if id else None

    if request.method == 'POST':
        nombre_refugio = request.POST.get('nombre_refugio', '').strip()
        direccion      = request.POST.get('direccion', '').strip()
        telefono       = request.POST.get('telefono', '').strip()
        email          = request.POST.get('email', '').strip()
        responsable    = request.POST.get('responsable', '').strip()
        capacidad      = request.POST.get('capacidad_maxima') or None
        descripcion    = request.POST.get('descripcion', '').strip()

        if not nombre_refugio or not direccion:
            messages.error(request, 'El nombre y la dirección son obligatorios.')
        else:
            if refugio is None:
                refugio = Refugio()

            refugio.nombre_refugio  = nombre_refugio
            refugio.direccion       = direccion
            refugio.telefono        = telefono
            refugio.email           = email
            refugio.responsable     = responsable
            refugio.capacidad_maxima = capacidad
            refugio.descripcion     = descripcion
            refugio.activo          = True

            # Foto del refugio
            if 'foto' in request.FILES:
                refugio.foto = request.FILES['foto']

            refugio.save()
            messages.success(request, f'Refugio "{refugio.nombre_refugio}" guardado correctamente.')
            return redirect('admin_refugios')

    return render(request, 'admin/refugios/form.html', {'refugio': refugio})


# ── ADMIN: ELIMINAR REFUGIO ───────────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN')
def admin_refugio_eliminar(request, id):
    refugio = get_object_or_404(Refugio, pk=id)
    try:
        nombre = refugio.nombre_refugio
        refugio.delete()
        messages.success(request, f'Refugio "{nombre}" eliminado.')
    except Exception:
        messages.error(request, 'No se puede eliminar. Tiene mascotas asociadas.')
    return redirect('admin_refugios')

@login_required
@rol_requerido('ADMIN')
def admin_refugio_toggle(request, id):
    if request.method == 'POST':
        refugio        = get_object_or_404(Refugio, pk=id)
        refugio.activo = not refugio.activo
        refugio.save()
        messages.success(request, f'Refugio {"activado" if refugio.activo else "desactivado"}')
    return redirect('admin_refugios')

@login_required
@rol_requerido('ADMIN')
def admin_reportes(request):
    return render(request, 'admin/reportes/reportes.html')

@login_required
@rol_requerido('ADMIN')
def reporte_mascotas_pdf(request):
    from .services.reporte_service import generar_reporte_mascotas_pdf
    pdf_bytes = generar_reporte_mascotas_pdf(request.GET.get('estado', ''))
    response  = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_mascotas.pdf"'
    return response

@login_required
@rol_requerido('ADMIN')
def reporte_adopciones_pdf(request):
    from .services.reporte_service import generar_reporte_adopciones_pdf
    fi        = request.GET.get('fechaInicio')
    ff        = request.GET.get('fechaFin')
    pdf_bytes = generar_reporte_adopciones_pdf(
        datetime.strptime(fi, '%Y-%m-%d').date() if fi else None,
        datetime.strptime(ff, '%Y-%m-%d').date() if ff else None
    )
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_adopciones.pdf"'
    return response

@login_required
@rol_requerido('ADMIN')
def reporte_mascotas_excel(request):
    from .services.reporte_service import generar_reporte_mascotas_excel
    excel_bytes = generar_reporte_mascotas_excel(request.GET.get('estado', ''))
    response    = HttpResponse(excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_mascotas.xlsx"'
    return response

@login_required
@rol_requerido('ADMIN')
def reporte_adopciones_excel(request):
    from .services.reporte_service import generar_reporte_adopciones_excel
    fi          = request.GET.get('fechaInicio')
    ff          = request.GET.get('fechaFin')
    excel_bytes = generar_reporte_adopciones_excel(
        datetime.strptime(fi, '%Y-%m-%d').date() if fi else None,
        datetime.strptime(ff, '%Y-%m-%d').date() if ff else None
    )
    response = HttpResponse(excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_adopciones.xlsx"'
    return response