from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'edad_aproximada': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'tamano': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado_salud': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'estado_adopcion': forms.Select(attrs={'class': 'form-control'}),
            'refugio': forms.Select(attrs={'class': 'form-control'}),
        }