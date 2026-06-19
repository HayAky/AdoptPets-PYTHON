import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password
from usuarios.models import Usuario
from refugios.models import Refugio
from mascotas.models import Mascota
from adopciones.models import Seguimiento, Adopcion

class UsuarioFactory(DjangoModelFactory):
    class Meta:
        model = Usuario
    email = factory.Sequence(lambda n: f'user{n}@email.com')
    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name')
    password = make_password('123')
    is_active = True

class RefugioFactory(DjangoModelFactory):
    class Meta:
        model = Refugio
    nombre_refugio = factory.Faker('company')
    usuario_encargado = factory.SubFactory(UsuarioFactory)

class MascotaFactory(DjangoModelFactory):
    class Meta:
        model = Mascota
    nombre = factory.Faker('first_name')
    color = 'Negro'
    refugio = factory.SubFactory(RefugioFactory)

class AdopcionFactory(DjangoModelFactory):
    class Meta:
        model = Adopcion
    adoptante = factory.SubFactory(UsuarioFactory)
    mascota = factory.SubFactory(MascotaFactory)
    fecha_solicitud = factory.Faker('date')
    estado_adopcion = 'PENDIENTE'

class SeguimientoFactory(DjangoModelFactory):
    class Meta:
        model = Seguimiento

    adopcion = factory.SubFactory(AdopcionFactory)
    tipo_contacto = 'llamada'
    estado_bienestar = 'bueno'