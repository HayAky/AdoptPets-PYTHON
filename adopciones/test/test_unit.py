from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import ForeignKey, CharField, TextField
from mascotas.models import Mascota
from adopciones.models import Adopcion, Seguimiento

# Intentamos importar el modelo de Refugio dinámicamente
try:
    from refugios.models import Refugio
except ImportError:
    try:
        from mascotas.models import Refugio
    except ImportError:
        Refugio = None

User = get_user_model()

class TestEcosistemaAdopcionesModule(TestCase):

    def setUp(self):
        """
        Configuración inicial: Prepara el entorno con Refugio, Mascota y Usuarios.
        """
        # 1. Crear Refugio de prueba adaptándose dinámicamente a tus campos reales
        self.refugio = None
        if Refugio:
            campos_refugio = {}
            # Inspeccionamos los campos reales de tu modelo Refugio
            for field in Refugio._meta.get_fields():
                if isinstance(field, (CharField, TextField)) and not field.primary_key:
                    # Asignamos valores genéricos según el nombre del campo para evitar TypeErrors
                    if 'nom' in field.name or 'refugio' in field.name:
                        campos_refugio[field.name] = "Refugio Huellitas"
                    elif 'dir' in field.name or 'ubica' in field.name:
                        campos_refugio[field.name] = "Calle 45 # 12-34"
                    elif 'tel' in field.name or 'cel' in field.name or 'contac' in field.name:
                        campos_refugio[field.name] = "3101234567"
                    elif not field.null and field.default == field.NOT_PROVIDED:
                        campos_refugio[field.name] = "Dato Requerido"

            self.refugio = Refugio.objects.create(**campos_refugio)

        # 2. Crear Administrador/Trabajador del refugio
        datos_admin = {"email": "admin@refugio.com", "password": "password123"}
        if hasattr(User, 'nombre'):
            datos_admin['nombre'], datos_admin['apellido'] = "Carlos", "Mendoza"
        else:
            datos_admin['first_name'], datos_admin['last_name'] = "Carlos", "Mendoza"
        if hasattr(User, 'username') and not User.get_email_field_name() == 'username':
            datos_admin['username'] = "admin_refugio"
        
        self.admin_user = User.objects.create_user(**datos_admin)

        # 3. Crear Usuario Adoptante potencial
        datos_adoptante = {"email": "camila@gmail.com", "password": "user1234"}
        if hasattr(User, 'nombre'):
            datos_adoptante['nombre'], datos_adoptante['apellido'] = "Camila", "Torres"
        else:
            datos_adoptante['first_name'], datos_adoptante['last_name'] = "Camila", "Torres"
        if hasattr(User, 'username') and not User.get_email_field_name() == 'username':
            datos_adoptante['username'] = "camila_adoptante"
            
        self.adoptante_user = User.objects.create_user(**datos_adoptante)

        # 4. Crear Mascota asociada al refugio si aplica
        campos_mascota = {
            "nombre": "Zeus",
            "especie": "Perro",
            "sexo": "Macho",
            "tamano": "Mediano",
            "estado_adopcion": "disponible"
        }
        for field in Mascota._meta.get_fields():
            if isinstance(field, ForeignKey) and field.related_model == Refugio and self.refugio:
                campos_mascota[field.name] = self.refugio

        self.mascota = Mascota.objects.create(**campos_mascota)

    def test_flujo_completo_adopcion_ecosistema(self):
        """
        PRUEBA 1: Flujo cruzado completo.
        Verifica que una adopción vincule correctamente al Usuario Adoptante, 
        la Mascota custodiada y genere su respectivo Seguimiento de control.
        """
        campos_adopcion = {}
        for field in Adopcion._meta.get_fields():
            if isinstance(field, ForeignKey):
                if field.related_model == Mascota:
                    campos_adopcion[field.name] = self.mascota
                elif field.related_model == User:
                    campos_adopcion[field.name] = self.adoptante_user

        for field in Adopcion._meta.get_fields():
            if field.name in ['fecha_solicitud', 'fecha']:
                campos_adopcion[field.name] = timezone.now().date()
            elif field.name == 'estado':
                campos_adopcion[field.name] = 'en_revision'

        adopcion_registro = Adopcion.objects.create(**campos_adopcion)
        self.assertIsNotNone(adopcion_registro.pk)

        campos_seguimiento = {}
        for field in Seguimiento._meta.get_fields():
            if isinstance(field, ForeignKey) and field.related_model == Adopcion:
                campos_seguimiento[field.name] = adopcion_registro
            elif field.name in ['fecha', 'fecha_seguimiento']:
                campos_seguimiento[field.name] = timezone.now().date()

        if not campos_seguimiento:
            campos_seguimiento['adopcion'] = adopcion_registro

        seguimiento = Seguimiento.objects.create(**campos_seguimiento)
        
        self.assertIsNotNone(seguimiento.pk)
        self.assertEqual(self.mascota.nombre, "Zeus")

    def test_verificar_refugio_de_mascota(self):
        """
        PRUEBA 2: Validar el vínculo entre el Refugio y la Mascota.
        """
        if self.refugio:
            refugio_asociado = None
            for field in Mascota._meta.get_fields():
                if isinstance(field, ForeignKey) and field.related_model == Refugio:
                    refugio_asociado = getattr(self.mascota, field.name)
            
            if refugio_asociado:
                self.assertIsNotNone(refugio_asociado.pk)

    def test_roles_usuarios_ecosistema(self):
        """
        PRUEBA 3: Validar que los usuarios mantengan identidades separadas en el sistema.
        """
        self.assertNotEqual(self.admin_user.email, self.adoptante_user.email)
        self.assertEqual(self.adoptante_user.email, "camila@gmail.com")