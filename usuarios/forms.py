from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Usuario


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class EditUsuarioForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'ciudad', 'cedula']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['old_password'].error_messages = {'password_incorrect': "La contraseña actual es incorrecta."}
        self.fields['new_password1'].error_messages = {'password_mismatch': "Las contraseñas no coinciden."}