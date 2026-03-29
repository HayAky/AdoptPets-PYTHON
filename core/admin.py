from django.contrib import admin
from .models import (
    Rol, Usuario, Refugio, Mascota, GaleriaFoto,
    Adopcion, Seguimiento, Noticia, Blog, Comentario
)

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Refugio)
admin.site.register(Mascota)
admin.site.register(GaleriaFoto)
admin.site.register(Adopcion)
admin.site.register(Seguimiento)
admin.site.register(Noticia)
admin.site.register(Blog)
admin.site.register(Comentario)