from django import forms
from .models import Ordenes_de_trabajo
from matafuegos.models import Matafuegos


class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = Ordenes_de_trabajo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#       self.fields['matafuegos'].queryset = Matafuegos.objects.none()
        #print(self.data)
        if 'cliente' in self.data:
         #   print('--------------HOLAAAA')
            try:
                id = int(self.data.get('cliente'))
                self.fields['matafuegos'].queryset = Matafuegos.objects.filter(cliente=id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
          #  print('-------------------')
            self.fields['matafuegos'].queryset = Matafuegos.objects.none()
        #print('-------------------CHAUUUU')
