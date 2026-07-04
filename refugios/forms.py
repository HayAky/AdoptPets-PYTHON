from django import forms
from .models import Refugio

LOCALIDADES_BOGOTA = [
    ("Usaquén", "Usaquén"), ("Chapinero", "Chapinero"), ("Santa Fe", "Santa Fe"),
    ("San Cristóbal", "San Cristóbal"), ("Usme", "Usme"), ("Tunjuelito", "Tunjuelito"),
    ("Bosa", "Bosa"), ("Kennedy", "Kennedy"), ("Fontibón", "Fontibón"),
    ("Engativá", "Engativá"), ("Suba", "Suba"), ("Barrios Unidos", "Barrios Unidos"),
    ("Teusaquillo", "Teusaquillo"), ("Los Mártires", "Los Mártires"),
    ("Antonio Nariño", "Antonio Nariño"), ("Puente Aranda", "Puente Aranda"),
    ("La Candelaria", "La Candelaria"), ("Rafael Uribe Uribe", "Rafael Uribe Uribe"),
    ("Ciudad Bolívar", "Ciudad Bolívar"), ("Sumapaz", "Sumapaz")
]

class RefugioForm(forms.ModelForm):
    localidad = forms.ChoiceField(
        choices=LOCALIDADES_BOGOTA,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Refugio
        fields = ['nombre_refugio', 'responsable', 'localidad', 'direccion',
                  'telefono', 'email', 'capacidad_maxima', 'descripcion',
                  'usuario_encargado', 'activo']
        widgets = {
            'nombre_refugio': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'usuario_encargado': forms.Select(attrs={'class': 'form-control'}),
        }
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