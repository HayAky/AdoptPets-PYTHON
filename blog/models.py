from django.db import models
from usuarios.models import Usuario


class CategoriaBlog(models.TextChoices):
    CUIDADO = 'CUIDADO', 'Cuidado'
    ENTRENAMIENTO = 'ENTRENAMIENTO', 'Entrenamiento'
    SALUD = 'SALUD', 'Salud'
    HISTORIAS = 'HISTORIAS', 'Historias'
    CONSEJOS = 'CONSEJOS', 'Consejos'


class CategoriaNoticia(models.TextChoices):
    ADOPCION = 'ADOPCION', 'Adopción'
    CUIDADO = 'CUIDADO', 'Cuidado'
    EVENTOS = 'EVENTOS', 'Eventos'
    SALUD = 'SALUD', 'Salud'
    GENERAL = 'GENERAL', 'General'


class Blog(models.Model):
    id_blog = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    resumen = models.CharField(max_length=255, null=True, blank=True)
    autor = models.CharField(max_length=255, null=True, blank=True)
    fecha_publicacion = models.DateField()
    activo = models.BooleanField(default=True)

    categoria = models.CharField(
        max_length=50,
        choices=CategoriaBlog.choices,
        null=True, blank=True
    )

    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    visitas = models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.titulo


class Noticia(models.Model):
    id_noticia = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    resumen = models.CharField(max_length=255, null=True, blank=True)
    autor = models.CharField(max_length=255, null=True, blank=True)
    fecha_publicacion = models.DateField()
    activa = models.BooleanField(default=True)

    categoria = models.CharField(
        max_length=50,
        choices=CategoriaNoticia.choices,
        null=True, blank=True
    )

    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'noticias'

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    id_comentario = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    tipo_contenido = models.CharField(max_length=50)  # "noticia" o "blog"

    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, null=True, blank=True, db_column='id_noticia')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, db_column='id_blog')

    comentario = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentarios'

    def __str__(self):
        return f"Comentario de {self.usuario.nombre}"