from django.db import models

class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=50, default='bogota')
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    roles = models.ManyToManyField(Rol, related_name='usuarios', db_table='usuarios_roles')

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"