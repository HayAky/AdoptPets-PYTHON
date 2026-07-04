from django.db.models.signals import post_save
from django.dispatch import receiver
from adopciones.models import Adopcion
from .models import HistorialActividad

@receiver(post_save, sender=Adopcion)
def registrar_adopcion(sender, instance, created, **kwargs):
    if created:
        HistorialActividad.objects.create(
            usuario=instance.adoptante,
            accion=f"Adopción: {instance.mascota.nombre}"
        )