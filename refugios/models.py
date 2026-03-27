from django.db import models

class Refugio(models.Model):
    id_refugio = models.BigAutoField(primary_key=True)
    nomrefugio = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    responsable = models.CharField(max_length=255, null=True, blank=True)
    capacidad_maxima = models.IntegerField(null=True, blank=True)
    localidad = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'refugios'

    def __str__(self):
        return self.nombre_refugio

