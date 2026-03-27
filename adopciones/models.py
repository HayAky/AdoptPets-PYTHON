from django.db import models
from usuarios.models import Usuario
from mascotas.models import Mascota, EstadoAdopcion

class Adopcion(models.Model):
    id_adopcion = models.BigAutoField(primary_key=True)

    adoptante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )

    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        db_column='id_mascota'
    )

    fecha_solicitud = models.DateField()
    fecha_aprobacion = models.DateField(null=True, blank=True)

    estado_adopcion = models.CharField(
        max_length=20,
        choices=EstadoAdopcion.choices,
        default=EstadoAdopcion.PENDIENTE
    )

    url_formulario_descarga = models.CharField(max_length=255, null=True, blank=True)
    formulario_enviado = models.BooleanField(default=False)
    fecha_envio_formulario = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fcha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'adopciones'

        def __str__(self):
            return f"Adopcion: {self.mascota.nombre} -> {self.adoptante.nombre}"


class TipoSeguimiento(models.TextChoices):
    LLAMADA = 'LLAMADA', 'Llamada'
    VISITA = 'VISITA', 'Visita'
    REPORTE_ADOPTANTE = 'REPORTE_ADOPTANTE', 'Reporte Adoptante'
    VETERINARIO = 'VETERINARIO', 'Veterinario'


class EstadoSaludMascota(models.TextChoices):
    BUENO = 'BUENO', 'Bueno'
    REGULAR = 'REGULAR', 'Regular'
    MALO = 'MALO', 'Malo'
    EN_TRATAMIENTO = 'EN_TRATAMIENTO', 'En Tratamiento'


class Seguimiento(models.Model):
    id_seguimiento = models.BigAutoField(primary_key=True)

    adoptante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_adoptante'
    )
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        db_column='id_mascota'
    )

    fecha_seguimiento = models.DateField()

    tipo_seguimiento = models.CharField(
        max_length=50,
        choices=TipoSeguimiento.choices
    )

    observaciones = models.TextField(null=True, blank=True)

    estado_mascota = models.CharField(
        max_length=50,
        choices=EstadoSaludMascota.choices,
        default=EstadoSaludMascota.BUENO
    )

    proximo_seguimiento = models.DateField(null=True, blank=True)
    realizado_por = models.CharField(max_length=255, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'seguimientos'

    def __str__(self):
        return f"Seguimiento {self.mascota.nombre} - {self.fecha_seguimiento}"