from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    # Esto le dice a Django: "lo que venga como 'edadAproximada' va al campo 'edad_aproximada'"
    edadAproximada = forms.IntegerField(source='edad_aproximada')

    class Meta:
        model = Mascota
        fields = '__all__'