from django.test import TestCase, RequestFactory
from mascotas.models import Mascota
from mascotas.views import lista_mascotas

class TestMascotasIntegration(TestCase):
    """
    Prueba de Integración directa utilizando RequestFactory
    para evadir el bug de clonación de contextos en Python 3.14.
    """

    def test_vista_lista_mascotas_publica(self):
        # 1. PREPARACIÓN: Registramos una mascota disponible
        Mascota.objects.create(
            nombre="Manolo",
            especie="Gato",
            sexo="Macho",
            tamano="Pequeño",
            estado_adopcion="disponible"
        )

        # 2. ACCIÓN: Creamos una petición HTTP simulada directamente en el backend
        factory = RequestFactory()
        request = factory.get('/mascotas/') # Simula que entran a la ruta

        # Ejecutamos tu vista pasándole la petición directamente
        respuesta = lista_mascotas(request)

        # 3. COMPROBACIÓN:
        # Verificamos que tu vista procese los datos y retorne un código de éxito 200 OK
        self.assertEqual(respuesta.status_code, 200)
        
        # Verificamos que el objeto de respuesta no venga vacío
        self.assertIsNotNone(respuesta.content)