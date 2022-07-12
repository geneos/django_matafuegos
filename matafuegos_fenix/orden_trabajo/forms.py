import self as self
from django import forms
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from cliente.models import Cliente
from matafuegos.models import Matafuegos



class OrdenesTrabajoAdminForm(forms.ModelForm):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=autocomplete.ModelSelect2(url='clientes-autocomplete',

    ))

    vencido = False
    matafuegos = forms.ModelChoiceField(
        queryset= Matafuegos.objects.all(),
        widget=autocomplete.ModelSelect2(url='matafuegos-autocomplete',
                                        forward=('cliente','vencido')
    ))
