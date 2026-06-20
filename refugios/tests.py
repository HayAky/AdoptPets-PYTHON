from django.test import TestCase, RequestFactory
from refugios.models import Refugio
from django.db.models import CharField

class TestRefugiosModule(TestCase):

    def test_crear_refugio_unitario(self):
        """
        Prueba Unitaria: Validar la creación de una fundación/refugio aliado
        detectando dinámicamente los nombres de tus campos CharField.
        """
        # 1. TRUCO DINÁMICO: Buscamos qué campos de texto tiene tu modelo Refugio
        campos_texto = [field.name for field in Refugio._meta.get_fields() if isinstance(field, CharField)]
        
        datos_refugio = {}
        valores_prueba = ["Fundación Huellitas Felices", "Calle 45 #12-34", "3001234567"]
        
        for i, nombre_campo in enumerate(campos_texto):
            if i < len(valores_prueba):
                datos_refugio[nombre_campo] = valores_prueba[i]

        # 2. Creamos el registro adaptado a tu modelo
        refugio = Refugio.objects.create(**datos_refugio)

        # 3. Comprobaciones
        self.assertIsNotNone(refugio.pk)
        
        if campos_texto:
            primer_campo = getattr(refugio, campos_texto[0])
            self.assertEqual(primer_campo, "Fundación Huellitas Felices")

    def test_vista_lista_refugios_integracion(self):
        """Prueba de Integración: Validar el procesamiento de la vista de refugios"""
        factory = RequestFactory()
        request = factory.get('/refugios/')
        
        # NOTA: Si tu vista en refugios/views.py se llama diferente a 'lista_refugios',
        # cambia el nombre aquí abajo:
        from refugios.views import lista_refugios
        
        respuesta = lista_refugios(request)
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsNotNone(respuesta.content)