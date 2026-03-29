from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# ─── ENUMS ───────────────────────────────────────────────────────────────────

class EstadoAdopcion(models.TextChoices):
    PENDIENTE  = 'pendiente',  'Pendiente'
    APROBADA   = 'aprobada',   'Aprobada'
    RECHAZADA  = 'rechazada',  'Rechazada'
    COMPLETADA = 'completada', 'Completada'
    DISPONIBLE = 'disponible', 'Disponible'
    EN_PROCESO = 'en_proceso', 'En Proceso'

class CategoriaBlog(models.TextChoices):
    CUIDADO       = 'CUIDADO',       'Cuidado'
    ENTRENAMIENTO = 'ENTRENAMIENTO', 'Entrenamiento'
    SALUD         = 'SALUD',         'Salud'
    HISTORIAS     = 'HISTORIAS',     'Historias'
    CONSEJOS      = 'CONSEJOS',      'Consejos'

class CategoriaNoticia(models.TextChoices):
    ADOPCION = 'ADOPCION', 'Adopción'
    CUIDADO  = 'CUIDADO',  'Cuidado'
    EVENTOS  = 'EVENTOS',  'Eventos'
    SALUD    = 'SALUD',    'Salud'
    GENERAL  = 'GENERAL',  'General'

class EstadoSaludMascota(models.TextChoices):
    EXCELENTE   = 'EXCELENTE',   'Excelente'
    BUENO       = 'BUENO',       'Bueno'
    REGULAR     = 'REGULAR',     'Regular'
    PREOCUPANTE = 'PREOCUPANTE', 'Preocupante'

class TipoSeguimiento(models.TextChoices):
    LLAMADA           = 'LLAMADA',           'Llamada'
    VISITA            = 'VISITA',            'Visita'
    REPORTE_ADOPTANTE = 'REPORTE_ADOPTANTE', 'Reporte Adoptante'
    VETERINARIO       = 'VETERINARIO',       'Veterinario'


# ─── ROL ─────────────────────────────────────────────────────────────────────

class Rol(models.Model):
    id_rol         = models.AutoField(primary_key=True)
    nombre_rol     = models.CharField(max_length=50, unique=True)
    descripcion    = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre_rol


# ─── USUARIO ─────────────────────────────────────────────────────────────────

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, nombre=nombre, apellido=apellido, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario       = models.AutoField(primary_key=True)
    nombre           = models.CharField(max_length=100)
    apellido         = models.CharField(max_length=100)
    email            = models.EmailField(max_length=150, unique=True)
    telefono         = models.CharField(max_length=20, blank=True, null=True)
    direccion        = models.CharField(max_length=255, blank=True, null=True)
    ciudad           = models.CharField(max_length=50, default='bogota')
    cedula           = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    activo           = models.BooleanField(default=True)
    fecha_registro   = models.DateTimeField(auto_now_add=True)
    roles            = models.ManyToManyField(Rol, related_name='usuarios_app', blank=True)
    is_staff         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.email})'

    def tiene_rol(self, nombre_rol):
        return self.roles.filter(nombre_rol=nombre_rol).exists()


# ─── REFUGIO ─────────────────────────────────────────────────────────────────

class Refugio(models.Model):
    id_refugio       = models.AutoField(primary_key=True)
    nombre_refugio   = models.CharField(max_length=150)
    direccion        = models.TextField()
    telefono         = models.CharField(max_length=20, blank=True, null=True)
    email            = models.CharField(max_length=150, blank=True, null=True)
    responsable      = models.CharField(max_length=100, blank=True, null=True)
    capacidad_maxima = models.IntegerField(blank=True, null=True)
    localidad        = models.CharField(max_length=50, blank=True, null=True)
    descripcion      = models.TextField(blank=True, null=True)
    activo           = models.BooleanField(default=True)
    fecha_registro   = models.DateTimeField(auto_now_add=True)
    foto             = models.ImageField(
        upload_to='refugios/', blank=True, null=True,
        verbose_name='Foto del refugio'
    )

    class Meta:
        db_table = 'refugios'

    def __str__(self):
        return self.nombre_refugio

    def get_foto_url(self):
        return self.foto.url if self.foto else None


# ─── MASCOTA ─────────────────────────────────────────────────────────────────

class Mascota(models.Model):
    id_mascota      = models.AutoField(primary_key=True)
    nombre          = models.CharField(max_length=100)
    especie         = models.CharField(max_length=100)
    raza            = models.CharField(max_length=100, blank=True, null=True)
    edad_aproximada = models.IntegerField(blank=True, null=True)
    sexo            = models.CharField(max_length=20)
    tamano          = models.CharField(max_length=20)
    peso            = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    color           = models.CharField(max_length=100, blank=True, null=True)
    descripcion     = models.TextField(blank=True, null=True)
    estado_salud    = models.TextField(blank=True, null=True)
    vacunado        = models.BooleanField(default=False)
    esterilizado    = models.BooleanField(default=False)
    microchip       = models.BooleanField(default=False)
    estado_adopcion = models.CharField(
        max_length=20, choices=EstadoAdopcion.choices,
        default=EstadoAdopcion.DISPONIBLE
    )
    fecha_ingreso   = models.DateField(blank=True, null=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)
    refugio         = models.ForeignKey(
        Refugio, on_delete=models.SET_NULL, null=True, related_name='mascotas'
    )
    foto_principal  = models.ImageField(
        upload_to='mascotas/', blank=True, null=True,
        verbose_name='Foto principal'
    )

    class Meta:
        db_table = 'mascotas'

    def __str__(self):
        return f'{self.nombre} ({self.especie})'

    def get_foto_url(self):
        return self.foto_principal.url if self.foto_principal else None


# ─── GALERÍA FOTOS ───────────────────────────────────────────────────────────

class GaleriaFoto(models.Model):
    id_foto      = models.AutoField(primary_key=True)
    foto         = models.ImageField(
        upload_to='mascotas/', blank=True, null=True, verbose_name='Foto'
    )
    url_foto     = models.CharField(max_length=500, blank=True, null=True)
    descripcion  = models.CharField(max_length=255, blank=True, null=True)
    es_principal = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    mascota      = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fotos')

    class Meta:
        db_table = 'galeria_fotos'

    def __str__(self):
        return f'Foto de {self.mascota.nombre}'

    def get_foto_url(self):
        if self.foto:
            return self.foto.url
        return self.url_foto


# ─── ADOPCIÓN ────────────────────────────────────────────────────────────────

class Adopcion(models.Model):
    id_adopcion             = models.AutoField(primary_key=True)
    adoptante               = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='adopciones')
    mascota                 = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='adopciones')
    fecha_solicitud         = models.DateField()
    fecha_aprobacion        = models.DateField(blank=True, null=True)
    estado_adopcion         = models.CharField(
        max_length=20, choices=EstadoAdopcion.choices, default=EstadoAdopcion.PENDIENTE
    )
    url_formulario_descarga = models.CharField(max_length=500, blank=True, null=True)
    formulario_enviado      = models.BooleanField(default=False)
    fecha_envio_formulario  = models.DateTimeField(blank=True, null=True)
    observaciones           = models.TextField(blank=True, null=True)
    fecha_registro          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'adopciones'

    def __str__(self):
        return f'Adopción #{self.id_adopcion} - {self.mascota.nombre}'


# ─── SEGUIMIENTO ─────────────────────────────────────────────────────────────

class Seguimiento(models.Model):
    id_seguimiento      = models.AutoField(primary_key=True)
    adoptante           = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguimientos')
    mascota             = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='seguimientos')
    fecha_seguimiento   = models.DateField()
    tipo_seguimiento    = models.CharField(max_length=30, choices=TipoSeguimiento.choices)
    observaciones       = models.TextField(blank=True, null=True)
    estado_mascota      = models.CharField(
        max_length=20, choices=EstadoSaludMascota.choices, default=EstadoSaludMascota.BUENO
    )
    proximo_seguimiento = models.DateField(blank=True, null=True)
    realizado_por       = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'seguimientos'

    def __str__(self):
        return f'Seguimiento #{self.id_seguimiento}'


# ─── NOTICIA ─────────────────────────────────────────────────────────────────

class Noticia(models.Model):
    id_noticia        = models.AutoField(primary_key=True)
    titulo            = models.CharField(max_length=200)
    contenido         = models.TextField()
    resumen           = models.CharField(max_length=500, blank=True, null=True)
    autor             = models.CharField(max_length=100, blank=True, null=True)
    fecha_publicacion = models.DateField()
    activa            = models.BooleanField(default=True)
    categoria         = models.CharField(
        max_length=20, choices=CategoriaNoticia.choices, blank=True, null=True
    )
    imagen_url        = models.CharField(max_length=500, blank=True, null=True)
    imagen            = models.ImageField(
        upload_to='noticias/', blank=True, null=True, verbose_name='Imagen'
    )
    fecha_registro    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'noticias'

    def __str__(self):
        return self.titulo

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url


# ─── BLOG ────────────────────────────────────────────────────────────────────

class Blog(models.Model):
    id_blog           = models.AutoField(primary_key=True)
    titulo            = models.CharField(max_length=200)
    contenido         = models.TextField()
    resumen           = models.CharField(max_length=500, blank=True, null=True)
    autor             = models.CharField(max_length=100, blank=True, null=True)
    fecha_publicacion = models.DateField()
    activo            = models.BooleanField(default=True)
    categoria         = models.CharField(
        max_length=20, choices=CategoriaBlog.choices, blank=True, null=True
    )
    imagen_url        = models.CharField(max_length=500, blank=True, null=True)
    imagen            = models.ImageField(
        upload_to='blog/', blank=True, null=True, verbose_name='Imagen'
    )
    visitas           = models.IntegerField(default=0)
    fecha_registro    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.titulo

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url


# ─── COMENTARIO ──────────────────────────────────────────────────────────────

class Comentario(models.Model):
    id_comentario    = models.AutoField(primary_key=True)
    usuario          = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    tipo_contenido   = models.CharField(max_length=20)
    noticia          = models.ForeignKey(
        Noticia, on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios'
    )
    blog             = models.ForeignKey(
        Blog, on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios'
    )
    comentario       = models.TextField()
    activo           = models.BooleanField(default=True)
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentarios'

    def __str__(self):
        return f'Comentario de {self.usuario.email}'