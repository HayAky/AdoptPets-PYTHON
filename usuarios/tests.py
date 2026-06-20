from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUsuariosModule(TestCase):

    def test_crear_usuario_unitario(self):
        """Prueba Unitaria: Validar el registro de un usuario usando el Email como identificador"""
        usuario = User.objects.create_user(
            email="fabian@test.com",
            password="password123",
            nombre="Fabián",
            apellido="Torres"
        )
        
        # Usamos .pk para que Django busque automáticamente tu llave primaria personalizada
        self.assertIsNotNone(usuario.pk)  
        self.assertEqual(usuario.email, "fabian@test.com")
        self.assertEqual(usuario.nombre, "Fabián")

    def test_vista_perfil_usuario_integracion(self):
        """Prueba de Integración: Simular petición HTTP a la vista de inicio"""
        # 1. Crear el usuario de prueba
        usuario = User.objects.create_user(
            email="test@test.com", 
            password="password123",
            nombre="Juan",
            apellido="Pérez"
        )
        
        # 2. Forzar la simulación de la petición en el backend
        factory = RequestFactory()
        request = factory.get('/usuarios/perfil/')
        request.user = usuario # Adjuntamos el usuario autenticado a la petición
        
        # 3. Importamos tu vista real de inicio desde mascotas
        from mascotas.views import inicio as vista_inicio
        
        respuesta = vista_inicio(request)
        
        # 4. Validar que el backend responda con éxito
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsNotNone(respuesta.content)