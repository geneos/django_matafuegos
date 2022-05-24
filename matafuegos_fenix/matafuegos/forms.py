from django import forms
from .models import Matafuegos

class ControlPatenteForm(forms.ModelForm):
    class Meta:
        model = Matafuegos
        fields = '__all__'

    def clean(self):
        if not self.cleaned_data.get('patente') and self.cleaned_data.get('categoria') is 'v':
            raise forms.ValidationError('Debe especificar la patente del vehiculo')
