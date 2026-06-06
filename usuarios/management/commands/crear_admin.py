from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Usuario.objects.filter(email='admin@adoptpets.com').exists():
            Usuario.objects.create_superuser(
                email='admin@adoptpets.com',
                nombre='Admin',
                apellido='Admin',
                password='admin314362'
            )
            self.stdout.write('Superusuario creado')
        else:
            self.stdout.write('Superusuario ya existe')
