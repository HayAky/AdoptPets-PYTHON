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