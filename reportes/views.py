from django.shortcuts import render
from django.utils import timezone
from .utils import generar_pdf
from mascotas.models import Mascota
from adopciones.models import Adopcion
from usuarios.models import Usuario
from refugios.models import Refugio
from usuarios.decorators import roles_permitidos


# ==========================================
# 1. REPORTE DE MASCOTAS
# ==========================================
@roles_permitidos(['ADMIN'])
def pdf_mascotas(request):
    mascotas = Mascota.objects.all().order_by('-fecha_registro')

    # Definimos las columnas
    columnas = ['Nombre', 'Especie', 'Raza', 'Estado', 'Refugio']

    # Extraemos los datos exactos que queremos en el PDF
    filas = [
        [
            m.nombre,
            m.especie,
            m.raza or 'N/A',
            m.get_estado_adopcion_display(),
            m.refugio.nombre_refugio if m.refugio else 'Sin asignar'
        ] for m in mascotas
    ]

    data = {
        'titulo': 'Reporte General de Mascotas',
        'fecha': timezone.now().strftime("%d/%m/%Y %H:%M"),
        'columnas': columnas,
        'filas': filas
    }
    return generar_pdf('reportes/pdf_base.html', data, 'AdoptPets_Mascotas.pdf')


# ==========================================
# 2. REPORTE DE ADOPCIONES
# ==========================================
@roles_permitidos(['ADMIN'])
def pdf_adopciones(request):
    adopciones = Adopcion.objects.all().order_by('-fecha_solicitud')
    columnas = ['ID', 'Mascota', 'Adoptante', 'Fecha Solicitud', 'Estado']

    filas = [
        [
            f"#{a.id_adopcion}",
            a.mascota.nombre,
            f"{a.adoptante.nombre} {a.adoptante.apellido}",
            a.fecha_solicitud.strftime("%d/%m/%Y"),
            a.get_estado_adopcion_display()
        ] for a in adopciones
    ]

    data = {
        'titulo': 'Historial de Solicitudes de Adopción',
        'fecha': timezone.now().strftime("%d/%m/%Y %H:%M"),
        'columnas': columnas,
        'filas': filas
    }
    return generar_pdf('reportes/pdf_base.html', data, 'AdoptPets_Adopciones.pdf')


# ==========================================
# 3. REPORTE DE USUARIOS
# ==========================================
@roles_permitidos(['ADMIN'])
def pdf_usuarios(request):
    usuarios = Usuario.objects.all().order_by('nombre')
    columnas = ['Nombre', 'Cédula', 'Email', 'Teléfono', 'Estado']

    filas = [
        [
            f"{u.nombre} {u.apellido}",
            u.cedula or 'N/A',
            u.email,
            u.telefono or 'N/A',
            "Activo" if u.is_active else "Inactivo"
        ] for u in usuarios
    ]

    data = {
        'titulo': 'Directorio de Usuarios Registrados',
        'fecha': timezone.now().strftime("%d/%m/%Y %H:%M"),
        'columnas': columnas,
        'filas': filas
    }
    return generar_pdf('reportes/pdf_base.html', data, 'AdoptPets_Usuarios.pdf')

@roles_permitidos(['ADMIN'])
def panel_reportes(request):
    # Esta es la vista que carga tu página con los botones
    return render(request, 'reportes/reportes.html')


# ==========================================
# 4. REPORTE DE REFUGIOS
# ==========================================
@roles_permitidos(['ADMIN'])
def pdf_refugios(request):
    refugios = Refugio.objects.all().order_by('nombre_refugio')
    columnas = ['Nombre', 'Responsable', 'Teléfono', 'Email', 'Estado']

    filas = [
        [
            r.nombre_refugio,
            r.responsable,
            r.telefono or 'N/A',
            r.email,
            "Activo" if r.activo else "Inactivo"
        ] for r in refugios
    ]

    data = {
        'titulo': 'Directorio de Refugios Aliados',
        'fecha': timezone.now().strftime("%d/%m/%Y %H:%M"),
        'columnas': columnas,
        'filas': filas
    }
    return generar_pdf('reportes/pdf_base.html', data, 'AdoptPets_Refugios.pdf')