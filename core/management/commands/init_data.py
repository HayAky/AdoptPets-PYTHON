from django.core.management.base import BaseCommand
from core.models import Rol, Usuario

class Command(BaseCommand):
    help = 'Inicializa roles y usuario administrador'

    def handle(self, *args, **kwargs):
        roles_data = [
            ('ROLE_ADMIN',     'Usuario con permisos completos del sistema'),
            ('ROLE_ADOPTANTE', 'Personas interesadas en adoptar mascotas'),
            ('ROLE_REFUGIO',   'Organizaciones que cuidan mascotas'),
        ]

        for nombre_rol, descripcion in roles_data:
            rol, created = Rol.objects.get_or_create(
                nombre_rol=nombre_rol,
                defaults={'descripcion': descripcion}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Rol "{nombre_rol}" creado.'))

        email_admin = 'admin@adoptpets.com'
        if not Usuario.objects.filter(email=email_admin).exists():
            admin = Usuario.objects.create_superuser(
                email=email_admin,
                nombre='Admin',
                apellido='Sistema',
                password='admin123'
            )
            rol_admin = Rol.objects.get(nombre_rol='ROLE_ADMIN')
            admin.roles.add(rol_admin)
            self.stdout.write(self.style.SUCCESS('🚀 Superusuario creado con éxito!'))
            self.stdout.write(f'📧 Email: {email_admin}')
            self.stdout.write(f'🔑 Contraseña: admin123')
        else:
            self.stdout.write(self.style.WARNING('⚠️ El superusuario ya existe.'))