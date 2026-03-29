from django.db import models
from refugios.models import Refugio

class EstadoAdopcion(models.TextChoices):
    DISPONIBLE = 'disponible', 'Disponible'
    PENDIENTE = 'pendiente', 'Pendiente'
    ADOPTADO = 'adoptado', 'Adoptado'


class Mascota(models.Model):
    id_mascota = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    especie = models.CharField(max_length=255)
    raza = models.CharField(max_length=255, null=True, blank=True)
    edad_aproximada = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=255)
    tamano = models.CharField(max_length=255)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    # ...
    color = models.CharField(max_length=50, null=True, blank=True)

    # NUEVO CAMPO DE IMAGEN
    foto = models.ImageField(upload_to='mascotas_fotos/', null=True, blank=True)

    descripcion = models.TextField(null=True, blank=True)
    # ...
    descripcion = models.TextField(null=True, blank=True)
    estado_salud = models.TextField(null=True, blank=True)
    vacunado = models.BooleanField(default=False)
    esterilizado = models.BooleanField(default=False)
    microchip = models.BooleanField(default=False)

    estado_adopcion = models.CharField(
        max_length=20,
        choices=EstadoAdopcion.choices,
        default=EstadoAdopcion.DISPONIBLE
    )

    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    refugio = models.ForeignKey(
        Refugio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mascotas',
        db_column='id_refugio'
    )

    class Meta:
        db_table = 'mascotas'

    def __str__(self):
        return f"{self.nombre} - {self.especie}"


class GaleriaFoto(models.Model):
    id_foto = models.BigAutoField(primary_key=True)
    url_foto = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    es_principal = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    mascota = models.ForeignKey(
        'Mascota',  # Usamos comillas porque la clase Mascota ya está definida arriba en este archivo
        on_delete=models.CASCADE,  # Si se borra la mascota, se borran sus fotos
        db_column='id_mascota',
        related_name='fotos'
    )

    class Meta:
        db_table = 'galeria_fotos'

    def __str__(self):
        return f"Foto de {self.mascota.nombre}"