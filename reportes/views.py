import csv
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

# Modelos para consultar los datos
from mascotas.models import Mascota
from adopciones.models import Adopcion
from usuarios.models import Usuario
from refugios.models import Refugio
from usuarios.decorators import roles_permitidos

# Importaciones para PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ==========================================
# 1. VISTA DEL PANEL DE REPORTES
# ==========================================
@roles_permitidos(['ADMIN'])
def panel_reportes(request):
    # Por defecto, la fecha de inicio es hace un mes
    fecha_fin = timezone.now().date()
    fecha_inicio = fecha_fin - timedelta(days=30)

    context = {
        'fechaInicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fechaFin': fecha_fin.strftime('%Y-%m-%d'),
    }
    return render(request, 'reportes/reportes.html', context)


# ==========================================
# 2. GENERADORES DE EXCEL (CSV)
# ==========================================
@roles_permitidos(['ADMIN'])
def reporte_mascotas_excel(request):
    estado = request.GET.get('estado', '')

    # Preparamos el archivo descargable
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_mascotas.csv"'

    # Escribimos los datos (usamos UTF-8 con BOM para que Excel lea las tildes)
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Especie', 'Raza', 'Estado', 'Refugio'])

    mascotas = Mascota.objects.all()
    if estado:
        mascotas = mascotas.filter(estado_adopcion=estado)

    for m in mascotas:
        refugio = m.refugio.nombre_refugio if m.refugio else "Sin asignar"
        writer.writerow([m.id_mascota, m.nombre, m.especie, m.raza, m.estado_adopcion, refugio])

    return response


@roles_permitidos(['ADMIN'])
def reporte_adopciones_excel(request):
    fecha_inicio = request.GET.get('fechaInicio')
    fecha_fin = request.GET.get('fechaFin')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_adopciones.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['ID', 'Fecha Solicitud', 'Mascota', 'Adoptante', 'Estado'])

    adopciones = Adopcion.objects.all()
    if fecha_inicio and fecha_fin:
        adopciones = adopciones.filter(fecha_solicitud__range=[fecha_inicio, fecha_fin])

    for a in adopciones:
        adoptante = f"{a.adoptante.nombre} {a.adoptante.apellido}"
        writer.writerow(
            [a.id_adopcion, a.fecha_solicitud.strftime('%Y-%m-%d'), a.mascota.nombre, adoptante, a.estado_adopcion])

    return response


# ==========================================
# 3. GENERADOR DE PDF BÁSICO
# ==========================================
@roles_permitidos(['ADMIN'])
def reporte_mascotas_pdf(request):
    estado = request.GET.get('estado', '')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_mascotas.pdf"'

    # Creamos el documento PDF
    p = canvas.Canvas(response, pagesize=letter)

    # Escribimos el título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Reporte Oficial de Mascotas - AdoptPets")

    # Dibujamos una línea divisoria
    p.line(50, 740, 550, 740)

    # Filtramos los datos
    mascotas = Mascota.objects.all()
    if estado:
        mascotas = mascotas.filter(estado_adopcion=estado)
        p.setFont("Helvetica", 10)
        p.drawString(50, 725, f"Filtro aplicado: {estado.upper()}")

    # Dibujamos las filas
    y = 700
    p.setFont("Helvetica", 10)
    for m in mascotas:
        texto = f"ID: {m.id_mascota} | Nombre: {m.nombre} | Especie: {m.especie} | Estado: {m.estado_adopcion}"
        p.drawString(50, y, texto)
        y -= 20  # Bajamos 20 pixeles para la siguiente línea

        # Si llegamos al final de la página, creamos una nueva
        if y < 50:
            p.showPage()
            y = 750

    p.save()
    return response


# ==========================================
# 4. GENERADORES FALTANTES (REFUGIOS Y USUARIOS)
# ==========================================
@roles_permitidos(['ADMIN'])
def reporte_refugios_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_refugios.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # Soporte para tildes
    writer = csv.writer(response)

    # Encabezados
    writer.writerow(['ID', 'Nombre de Fundación', 'Localidad', 'Teléfono', 'Email', 'Capacidad Máxima', 'Estado'])

    for r in Refugio.objects.all():
        estado = "Activo" if r.activo else "Inactivo"
        writer.writerow([r.id_refugio, r.nombre_refugio, r.localidad, r.telefono, r.email, r.capacidad_maxima, estado])

    return response


@roles_permitidos(['ADMIN'])
def reporte_usuarios_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)

    # Encabezados
    writer.writerow(['ID', 'Nombre', 'Apellido', 'Cédula', 'Email', 'Teléfono', 'Roles'])

    for u in Usuario.objects.all():
        # Juntamos los roles en un solo texto (Ej: "ADMIN, REFUGIO")
        roles = ", ".join([rol.nombre_rol for rol in u.roles.all()])
        writer.writerow([u.id, u.nombre, u.apellido, u.cedula, u.email, u.telefono, roles])

    return response


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@roles_permitidos(['ADMIN'])
def reporte_adopciones_pdf(request):
    fecha_inicio = request.GET.get('fechaInicio')
    fecha_fin = request.GET.get('fechaFin')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_adopciones.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Reporte de Adopciones - AdoptPets")
    p.line(50, 740, 550, 740)

    adopciones = Adopcion.objects.all()
    if fecha_inicio and fecha_fin:
        adopciones = adopciones.filter(fecha_solicitud__range=[fecha_inicio, fecha_fin])
        p.setFont("Helvetica", 10)
        p.drawString(50, 725, f"Periodo: {fecha_inicio} a {fecha_fin}")

    y = 700
    p.setFont("Helvetica", 10)
    for a in adopciones:
        texto = f"Fecha: {a.fecha_solicitud.strftime('%Y-%m-%d')} | Mascota: {a.mascota.nombre} | Adoptante: {a.adoptante.nombre} {a.adoptante.apellido} | Estado: {a.estado_adopcion}"
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.save()
    return response


@roles_permitidos(['ADMIN'])
def reporte_refugios_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_refugios.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Directorio de Refugios Aliados")
    p.line(50, 740, 550, 740)

    y = 710
    p.setFont("Helvetica", 10)
    for r in Refugio.objects.all():
        estado = "ACTIVO" if r.activo else "INACTIVO"
        texto = f"[{estado}] {r.nombre_refugio} | Loc: {r.localidad} | Tel: {r.telefono}"
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.save()
    return response


@roles_permitidos(['ADMIN'])
def reporte_usuarios_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_usuarios.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Listado de Usuarios del Sistema")
    p.line(50, 740, 550, 740)

    y = 710
    p.setFont("Helvetica", 10)
    for u in Usuario.objects.all():
        roles = ", ".join([rol.nombre_rol for rol in u.roles.all()])
        texto = f"{u.nombre} {u.apellido} | Email: {u.email} | Roles: {roles}"
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.save()
    return response