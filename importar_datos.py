import os
import django
from datetime import datetime

# Configurar el entorno de Django para poder usar los modelos desde este archivo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adopt_pets.settings')
django.setup()

# Importar los modelos
from refugios.models import Refugio
from mascotas.models import Mascota
from mascotas.models import Mascota, GaleriaFoto
from blog.models import Noticia, Blog, Comentario
from usuarios.models import Usuario

def poblar_base_de_datos():
    print("Iniciando importación de datos...")

    # ==========================================
    # 1. INSERTAR REFUGIOS
    # ==========================================
    refugios_data = [
        (1, 'Fundación Protectora de Animales Bogotá', 'Calle 26 #68-35, Zona Industrial', '601-234-5678', 'info@protectorabogota.org', 'María González', 50, 'Puente Aranda', 'Refugio especializado en perros y gatos abandonados'),
        (2, 'Hogar de Paso San Francisco', 'Carrera 15 #127-45, Usaquén', '601-345-6789', 'contacto@hogarsanfrancisco.com', 'Carlos Rodríguez', 30, 'Usaquén', 'Centro de rescate y rehabilitación animal'),
        (3, 'Refugio Patitas Felices', 'Calle 170 #45-23, Suba', '601-456-7890', 'patitasfelices@gmail.com', 'Ana Martínez', 40, 'Suba', 'Refugio familiar especializado en cachorros'),
        (4, 'Fundación Amor Animal Chapinero', 'Carrera 13 #85-67, Chapinero', '601-567-8901', 'amoranimal@outlook.com', 'Luis Hernández', 25, 'Chapinero', 'Refugio urbano para animales rescatados'),
        (5, 'Centro de Adopción La Candelaria', 'Calle 10 #3-45, La Candelaria', '601-678-9012', 'adopcion@lacandelaria.org', 'Patricia López', 35, 'La Candelaria', 'Centro histórico de adopción animal'),
        (6, 'Refugio Esperanza Animal', 'Calle 80 #115-20, Engativá', '601-789-0123', 'esperanza@animalrefugio.com', 'Roberto Silva', 60, 'Engativá', 'Refugio con programas de esterilización'),
        (7, 'Hogar Temporal Fontibón', 'Carrera 100 #25-15, Fontibón', '601-890-1234', 'temporal@fontibon.net', 'Sandra Ramírez', 20, 'Fontibón', 'Hogar temporal especializado en gatos'),
        (8, 'Fundación Rescate Animal Sur', 'Calle 38 Sur #27-45, San Cristóbal', '601-901-2345', 'rescatesur@gmail.com', 'Diego Morales', 45, 'San Cristóbal', 'Refugio comunitario del sur de Bogotá'),
        (9, 'Centro Protección Animal Kennedy', 'Carrera 78 #38-20, Kennedy', '601-012-3456', 'proteccion@kennedy.org', 'Elena Vargas', 55, 'Kennedy', 'Centro integral de protección animal'),
        (10, 'Refugio Amigos de Cuatro Patas', 'Calle 134 #52-18, Barrios Unidos', '601-123-4567', 'cuatropatas@hotmail.com', 'Fernando Castro', 30, 'Barrios Unidos', 'Refugio familiar con adopciones responsables')
    ]

    for r in refugios_data:
        Refugio.objects.update_or_create(id_refugio=r[0], defaults={
            'nombre_refugio': r[1], 'direccion': r[2], 'telefono': r[3], 'email': r[4],
            'responsable': r[5], 'capacidad_maxima': r[6], 'localidad': r[7],
            'descripcion': r[8], 'activo': True
        })
    print(f"✅ Se insertaron {len(refugios_data)} refugios.")


    # 2. INSERTAR MASCOTAS Y GALERIA_FOTOS

    mascotas_data = [
        # id, nombre, especie, raza, edad, sexo, tamaño, peso, color, descripcion, estado_salud, vacunado, esterilizado, microchip, fecha, id_refugio, url_foto_principal
        (1, 'Luna', 'perro', 'Mestizo', 2, 'hembra', 'mediano', 15.5, 'Negro con blanco',
         'Perra muy cariñosa y tranquila, ideal para familias', 'Excelente estado de salud', True, True, True,
         '2024-11-15', 1, '/static/img/Luna.jpg'),
        (2, 'Max', 'perro', 'Golden Retriever', 3, 'macho', 'grande', 28.0, 'Dorado',
         'Perro muy activo y juguetón, ama a los niños', 'Excelente, solo necesita ejercicio regular', True, True,
         False, '2024-12-01', 2, '/static/img/Max.jpg'),
        (3, 'Mimi', 'gato', 'Siamés', 1, 'hembra', 'pequeño', 3.2, 'Crema con puntos oscuros',
         'Gata muy elegante e independiente', 'Perfecta salud', True, True, True, '2024-11-20', 7,
         '/static/img/Mimi.jpg'),
        (4, 'Rocky', 'perro', 'Pitbull', 4, 'macho', 'grande', 25.8, 'Gris',
         'Perro protector pero muy dulce con su familia', 'Buena salud, tratamiento preventivo parasitos', True, True,
         True, '2024-10-30', 3, '/static/img/Rocky.jpg'),
        (5, 'Pelusa', 'gato', 'Persa', 5, 'hembra', 'mediano', 4.5, 'Blanco',
         'Gata tranquila, perfecta para apartamentos', 'Excelente, cuidado especial del pelaje', True, True, False,
         '2024-11-10', 4, '/static/img/Pelusa.jpeg'),
        (6, 'Buddy', 'perro', 'Labrador', 2, 'macho', 'grande', 30.2, 'Chocolate',
         'Perro muy inteligente y fácil de entrenar', 'Excelente estado físico', True, False, True, '2024-12-05', 5,
         '/static/img/Buddy.png'),
        (7, 'Nala', 'gato', 'Mestizo', 3, 'hembra', 'pequeño', 3.8, 'Atigrado', 'Gata muy sociable y juguetona',
         'Perfecta salud', True, True, True, '2024-11-25', 6, '/static/img/Nala.jpg'),
        (8, 'Thor', 'perro', 'Pastor Alemán', 6, 'macho', 'grande', 35.0, 'Negro con café',
         'Perro maduro, tranquilo y obediente', 'Buena salud, chequeos regulares por edad', True, True, True,
         '2024-10-15', 8, '/static/img/Thor.jpg'),
        (9, 'Coco', 'conejo', 'Mini Lop', 1, 'macho', 'pequeño', 1.2, 'Café claro', 'Conejo muy dócil y cariñoso',
         'Excelente salud', True, True, False, '2024-11-30', 9, '/static/img/Coco.jpg'),
        (10, 'Princesa', 'gato', 'Ragdoll', 2, 'hembra', 'mediano', 4.0, 'Gris con blanco',
         'Gata muy tranquila y cariñosa', 'Perfecta salud', True, True, True, '2024-12-08', 10,
         '/static/img/Princesa.jpg')
    ]

    for m in mascotas_data:
        refugio = Refugio.objects.get(id_refugio=m[15])

        mascota, created = Mascota.objects.update_or_create(id_mascota=m[0], defaults={
            'nombre': m[1], 'especie': m[2], 'raza': m[3], 'edad_aproximada': m[4],
            'sexo': m[5], 'tamano': m[6], 'peso': m[7], 'color': m[8],
            'descripcion': m[9], 'estado_salud': m[10], 'vacunado': m[11],
            'esterilizado': m[12], 'microchip': m[13], 'fecha_ingreso': m[14],
            'estado_adopcion': 'disponible', 'refugio': refugio
        })

        if m[16]:
            GaleriaFoto.objects.update_or_create(
                mascota=mascota,
                url_foto=m[16],
                defaults={
                    'es_principal': True,
                    'descripcion': f'Foto principal de {mascota.nombre}'
                }
            )

    print(f"✅ Se insertaron {len(mascotas_data)} mascotas y sus fotos en Galería.")

    # ==========================================
    # 3. INSERTAR NOTICIAS Y BLOGS
    # ==========================================
    Noticia.objects.update_or_create(id_noticia=1, defaults={
        'titulo': 'Campaña de esterilización gratuita en Bogotá',
        'contenido': 'La alcaldía de Bogotá lanza una nueva campaña de esterilización para mascotas rescatadas...',
        'resumen': 'Campaña gratuita para esterilizar mascotas en toda la ciudad.', 'autor': 'Redacción',
        'fecha_publicacion': '2024-12-01', 'categoria': 'SALUD',
        'imagen_url': '/static/img/Esterilizar_mascotas.png'
    })
    Noticia.objects.update_or_create(id_noticia=2, defaults={
        'titulo': 'Récord de adopciones en diciembre',
        'contenido': 'Este mes hemos logrado un récord histórico en nuestro sistema con cientos de finales felices...',
        'resumen': 'Más de 200 mascotas encontraron hogar este mes.', 'autor': 'María González',
        'fecha_publicacion': '2024-12-15', 'categoria': 'ADOPCION',
        'imagen_url': '/static/img/perrosygatos.png'
    })

    Blog.objects.update_or_create(id_blog=1, defaults={
        'titulo': 'Cómo preparar tu casa para una nueva mascota',
        'contenido': 'Adoptar una mascota es una decisión importante. Asegúrate de tener un espacio limpio y seguro...',
        'resumen': 'Guía completa para preparar el hogar antes de la llegada de tu nueva mascota.',
        'autor': 'Dr. Carlos (Veterinario)', 'fecha_publicacion': '2024-11-20', 'categoria': 'CONSEJOS',
        'imagen_url': '/static/img/Wel_adopcion-virtual-animales.jpg'
    })
    Blog.objects.update_or_create(id_blog=2, defaults={
        'titulo': 'La historia de Max: De abandono a amor',
        'contenido': 'Max llegó a nuestro refugio en muy mal estado, pero con paciencia y una buena familia logró recuperarse...',
        'resumen': 'Historia inspiradora de rescate y adopción exitosa.', 'autor': 'Ana Martínez',
        'fecha_publicacion': '2024-12-05', 'categoria': 'HISTORIAS',
        'imagen_url': '/static/img/Max.jpg'
    })
    print("✅ Se insertaron Noticias y Blogs.")

    # ==========================================
    # 4. INSERTAR COMENTARIOS (Opcional, protegido)
    # ==========================================
    try:
        # Busca el primer usuario administrador o cualquier usuario que tengas registrado
        # para asignarle los comentarios y que no haya error si no existen los IDs 1,3,5,7.
        usuario_demo = Usuario.objects.first()
        if usuario_demo:
            Comentario.objects.create(usuario=usuario_demo, tipo_contenido='noticia', noticia_id=1, comentario='Excelente iniciativa, mi perro fue esterilizado en una campaña similar.')
            Comentario.objects.create(usuario=usuario_demo, tipo_contenido='blog', blog_id=1, comentario='Muy buenos consejos, me ayudaron mucho antes de adoptar a mi gata.')
            Comentario.objects.create(usuario=usuario_demo, tipo_contenido='noticia', noticia_id=2, comentario='¡Qué alegría saber que tantas mascotas encontraron hogar!')
            Comentario.objects.create(usuario=usuario_demo, tipo_contenido='blog', blog_id=2, comentario='Historias como esta me motivan a seguir apoyando los refugios.')
            print("✅ Se insertaron los Comentarios usando un usuario de prueba.")
    except Exception as e:
        print(f"⚠️ No se insertaron comentarios por un error de usuarios: {e}")

    print("🎉 ¡BASE DE DATOS POBLADA CON ÉXITO!")

if __name__ == '__main__':
    poblar_base_de_datos()