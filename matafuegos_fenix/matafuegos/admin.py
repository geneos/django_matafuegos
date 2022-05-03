from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import CategoriaMatafuegos, TipoMatafuegos, MarcaMatafuegos, Matafuegos
from .forms import ControlPatenteForm

class MatafuegosResource(resources.ModelResource):

    class Meta:
        model = Matafuegos

class MatafuegosAdmin(ImportExportModelAdmin):

    list_display = (
        'numero',
        'numero_dps',
        'fecha_proxima_carga',
        'fecha_proxima_ph',
    )
    form = ControlPatenteForm
    search_fields= ('numero', 'numero_dps',)
    list_filter= ('marca',)
    readonly_fields=['fecha_proxima_carga','fecha_proxima_ph']
    resource_class = MatafuegosResource

class TipoMatafuegosAdmin(admin.ModelAdmin):
    list_display = (
        'tipo',
        'categoria',
        'vencimiento_carga',
        'vencimiento_ph',
        'volumen',
        'peso',
    )
    search_fields= ('tipo',)
    list_filter= ('categoria',)

admin.site.register(CategoriaMatafuegos)
admin.site.register(TipoMatafuegos, TipoMatafuegosAdmin)
admin.site.register(MarcaMatafuegos)
admin.site.register(Matafuegos, MatafuegosAdmin)
