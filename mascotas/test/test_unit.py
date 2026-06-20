import pytest
from mascotas.models import Mascota, EstadoAdopcion

@pytest.mark.django_db
def test_crear_mascota_unitaria():
    """Prueba Unitaria: Verifica la creación de una mascota usando tu modelo real"""
    
    # 1. ACCIÓN: Creamos la mascota con los campos obligatorios de tu modelo
    nueva_mascota = Mascota.objects.create(
        nombre="Rambo",
        especie="Perro",
        sexo="Macho",
        tamano="Mediano",
        edad_aproximada=3,
        vacunado=True
    )
    
    # 2. COMPROBACIÓN (Asserts): Comparamos lo que se guardó contra lo que esperas
    # Verificamos que Django le asigne automáticamente su llave primaria (id_mascota)
    assert nueva_mascota.id_mascota is not None 
    
    # Verificamos que el nombre guardado sea el correcto
    assert nueva_mascota.nombre == "Rambo"
    
    # Verificamos que tome el estado por defecto que definiste: DISPONIBLE ('disponible')
    assert nueva_mascota.estado_adopcion == EstadoAdopcion.DISPONIBLE