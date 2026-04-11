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
    TIPO_CONTACTO_CHOICES = [
        ('visita', 'Visita Presencial'),
        ('llamada', 'Llamada Telefónica'),
        ('whatsapp', 'Mensaje / WhatsApp'),
        ('correo', 'Correo Electrónico'),
    ]

    ESTADO_BIENESTAR_CHOICES = [
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular (Requiere atención)'),
        ('critico', 'Crítico / Peligro'),
    ]

    # Relación principal: Un seguimiento pertenece a una adopción específica
    adopcion = models.ForeignKey('Adopcion', on_delete=models.CASCADE, related_name='seguimientos', null=True,
                                 blank=True)
    # Datos de la bitácora
    fecha_contacto = models.DateField(auto_now_add=True)
    tipo_contacto = models.CharField(max_length=20, choices=TIPO_CONTACTO_CHOICES, default='llamada')
    observaciones = models.TextField(null=True, blank=True, help_text="Detalles de la adaptación, comportamiento, etc.")
    estado_bienestar = models.CharField(max_length=20, choices=ESTADO_BIENESTAR_CHOICES, default='bueno')

    # Planificación a futuro (Opcional)
    proxima_fecha = models.DateField(null=True, blank=True, help_text="¿Cuándo se debe volver a contactar?")

    def __str__(self):
        return f"Seguimiento {self.id} - {self.adopcion.mascota.nombre} ({self.fecha_contacto})"