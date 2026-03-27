from django.db import models

class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
