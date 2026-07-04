from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Refugio, Usuario

# --- MIXIN PARA ESTILOS ---
class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# --- FORMULARIOS ---

# forms.py
class EditUsuarioForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'telefono']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and (len(telefono) < 7 or not telefono.isdigit()):
            raise forms.ValidationError("Ingrese un número de teléfono válido (mínimo 7 dígitos).")
        return telefono

class RefugioForm(FormStyleMixin, forms.ModelForm):
    # Definimos el campo de localidad explícitamente para mantener la lista de opciones
    localidad = forms.ChoiceField(
        choices=[
            ("Usaquén", "Usaquén"), ("Chapinero", "Chapinero"), ("Santa Fe", "Santa Fe"),
            ("San Cristóbal", "San Cristóbal"), ("Usme", "Usme"), ("Tunjuelito", "Tunjuelito"),
            ("Bosa", "Bosa"), ("Kennedy", "Kennedy"), ("Fontibón", "Fontibón"),
            ("Engativá", "Engativá"), ("Suba", "Suba"), ("Barrios Unidos", "Barrios Unidos"),
            ("Teusaquillo", "Teusaquillo"), ("Los Mártires", "Los Mártires"),
            ("Antonio Nariño", "Antonio Nariño"), ("Puente Aranda", "Puente Aranda"),
            ("La Candelaria", "La Candelaria"), ("Rafael Uribe Uribe", "Rafael Uribe Uribe"),
            ("Ciudad Bolívar", "Ciudad Bolívar"), ("Sumapaz", "Sumapaz")
        ]
    )

    class Meta:
        model = Refugio
        fields = ['nombre_refugio', 'responsable', 'localidad', 'direccion',
                  'telefono', 'email', 'capacidad_maxima', 'descripcion',
                  'activo', 'usuario_encargado']

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario que pasamos desde la vista
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Lógica de seguridad: Si el usuario NO es admin, bloqueamos el campo
        if self.user and not self.user.es_admin:
            self.fields['usuario_encargado'].disabled = True

    # Validación estricta de correo
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and "@" not in email:
            raise forms.ValidationError("El correo debe contener un '@' válido.")
        return email

    # Validación de números
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar estilos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Sobrescribir mensajes de error al español
        self.fields['old_password'].error_messages = {
            'password_incorrect': "La contraseña actual es incorrecta."
        }
        self.fields['new_password1'].error_messages = {
            'password_mismatch': "Las contraseñas no coinciden."
        }