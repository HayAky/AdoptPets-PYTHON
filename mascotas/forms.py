from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    # Esto le dice a Django: "lo que venga como 'edadAproximada' va al campo 'edad_aproximada'"
    # En forms.py
    edadAproximada = forms.IntegerField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.edad_aproximada = self.cleaned_data['edadAproximada']
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Mascota
        fields = '__all__'