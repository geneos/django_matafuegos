from django.contrib import admin

# Register your models here.
from .models import Tarea, Ordenes_de_trabajo, Tarea_Orden


class TareaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'precio',
    )

class TareaTabularInline(admin.TabularInline):
    model = Tarea_Orden
    can_delete = True

class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'fecha',
        'fecha_entrega',
        'cliente',
        'estado',
        'monto_total'
    )
    inlines = [TareaTabularInline]
    readonly_fields = ['monto_total']

class TareaOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'tarea',
        'orden'
    )



admin.site.register(Ordenes_de_trabajo, OrdenTrabajoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Tarea_Orden, TareaOrdenAdmin)
