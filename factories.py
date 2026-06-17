# factories.py
import factory
from mascotas.models import Mascota
from usuarios.models import Usuario

class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
    email = factory.Sequence(lambda n: f'user{n}@test.com')
    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name')
    password = '123'

class MascotaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mascota
    # Ajusta los campos según tu modelo exacto
    nombre = factory.Faker('first_name')
    color = 'Negro'
    # Si la mascota requiere una llave foránea (ej. refugio), se enlaza así:
    # refugio = factory.SubFactory(RefugioFactory)