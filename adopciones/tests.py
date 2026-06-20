# LÍNEAS 1 A 6: Primero le explicamos a Python qué herramientas vamos a usar
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import ForeignKey
from mascotas.models import Mascota
from adopciones.models import Adopcion, Seguimiento

# LÍNEA 8: Definimos qué es 'User' antes de que empiece la prueba
User = get_user_model()

# LÍNEA 10 en adelante: Estructura de la prueba
class TestAdopcionesModule(TestCase):

    def test_crear_seguimiento_adopcion_integrado(self):
        """
        Prueba de Integración: Flujo completo automatizado.
        Detecta las llaves foráneas y asigna los campos obligatorios de fecha.
        """
        
        # 1. Crear el usuario adoptante de forma segura
        datos_usuario = {
            "email": "juan@adopta.com",
            "password": "password123"
        }
        
        if hasattr(User, 'nombre'):
            datos_usuario['nombre'] = "Juan"
            datos_usuario['apellido'] = "Castro"
        else:
            datos_usuario['first_name'] = "Juan"
            datos_usuario['last_name'] = "Castro"
            
        if hasattr(User, 'username') and not User.get_email_field_name() == 'username':
            datos_usuario['username'] = "juan_adopta"

        adoptante = User.objects.create_user(**datos_usuario)
        
        # 2. Crear la mascota de prueba
        mascota = Mascota.objects.create(
            nombre="Toby",
            especie="Perro",
            sexo="Macho",
            tamano="Grande",
            estado_adopcion="pendiente"
        )
        
        # 3. Mapeamos los campos dinámicos de la Adopción
        campos_adopcion = {}
        for field in Adopcion._meta.get_fields():
            if isinstance(field, ForeignKey):
                if field.related_model == Mascota:
                    campos_adopcion[field.name] = mascota
                elif field.related_model == User:
                    campos_adopcion[field.name] = adoptante

        # 4. Agregamos la fecha de solicitud obligatoria
        for field in Adopcion._meta.get_fields():
            if field.name in ['fecha_solicitud', 'fecha']:
                campos_adopcion[field.name] = timezone.now().date()

        adopcion_registro = Adopcion.objects.create(**campos_adopcion)
        
        # 5. Crear el Seguimiento apuntando a la Adopción
        campos_seguimiento = {}
        for field in Seguimiento._meta.get_fields():
            if isinstance(field, ForeignKey) and field.related_model == Adopcion:
                campos_seguimiento[field.name] = adopcion_registro
            elif field.name in ['fecha', 'fecha_seguimiento']:
                campos_seguimiento[field.name] = timezone.now().date()
            elif field.name == 'estado':
                campos_seguimiento[field.name] = "En Proceso"

        if not campos_seguimiento:
            campos_seguimiento['adopcion'] = adopcion_registro

        seguimiento = Seguimiento.objects.create(**campos_seguimiento)
        
        # 6. Comprobaciones finales
        self.assertIsNotNone(seguimiento.pk)
        
        for field_name, val in campos_adopcion.items():
            if isinstance(val, Mascota):
                objeto_mascota = getattr(adopcion_registro, field_name)
                self.assertEqual(objeto_mascota.nombre, "Toby")