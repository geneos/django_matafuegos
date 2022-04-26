from django.contrib import admin

# Register your models here.
from .models import CategoriaMatafuegos, TipoMatafuegos, MarcaMatafuegos, Matafuegos

class MatafuegosAdmin(admin.ModelAdmin):

    list_display = (
        'numero',
        'numero_bv',
        'numero_dps',
        'fecha_proxima_carga',
        'fecha_proxima_ph',
    )

    search_fields= ('numero', 'numero_bv', 'numero_dps',)
    list_filter= ('marca',)

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


