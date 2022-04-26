from django.contrib import admin

# Register your models here.
from .models import Parametros


class ParametrosAdmin(admin.ModelAdmin):
    list_display = (
        'veh_inicio',
        'veh_fin',
        'veh_prefijo',
        'veh_actual',
        'dom_inicio',
        'dom_fin',
        'dom_prefijo',
        'dom_actual',
    )

admin.site.register(Parametros, ParametrosAdmin)
