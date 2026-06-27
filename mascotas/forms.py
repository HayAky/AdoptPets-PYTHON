from django import forms
from .models import Mascota

from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    # Define tus listas aquí
    ESPECIE_CHOICES = [('perro', 'Perro'), ('gato', 'Gato'), ('conejo', 'Conejo'), ('otro', 'Otro')]
    SEXO_CHOICES = [('macho', 'Macho'), ('hembra', 'Hembra')]
    TAMANO_CHOICES = [('pequeño', 'Pequeño'), ('mediano', 'Mediano'), ('grande', 'Grande')]
    ESTADO_ADOPCION_CHOICES = [('disponible', 'Disponible'), ('pendiente', 'Pendiente'), ('adoptado', 'Adoptado')]

    # Sobrescribe los campos para forzar que sean selectores (dropdowns)
    especie = forms.ChoiceField(choices=ESPECIE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    tamano = forms.ChoiceField(choices=TAMANO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    estado_adopcion = forms.ChoiceField(choices=ESTADO_ADOPCION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Mascota
        fields = '__all__' # O la lista de todos tus campos
        # Mantén los widgets para los campos que NO son listas (como nombre, foto, etc.)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            # ... resto de widgets normales ...
        }
        widgets = {
            # Aquí inyectas las clases CSS que tenías antes para recuperar el estilo
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'edad_aproximada': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'tamano': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'estado_salud': forms.Textarea(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }