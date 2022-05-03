from datetime import date

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
    readonly_fields = ('tarea',)
    fields = ('tarea',)


@admin.action(description='Iniciar orden de trabajo')
def action_iniciada(modeladmin, request, queryset):
    queryset.update(estado='ep')
<<<<<<< Updated upstream
    queryset.update(fecha_inicio=date.today())
    queryset.update(fecha_cierre=None)
=======
    queryset.update(fecha_cierre = None)
>>>>>>> Stashed changes

@admin.action(description='Finalizar orden de trabajo')
def action_finalizada(modeladmin, request, queryset):
    queryset.update(estado='f')
    queryset.update(fecha_cierre=date.today())

@admin.action(description='Cancelar orden de trabajo')
def action_cancelada(modeladmin, request, queryset):
    queryset.update(estado='c')

class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha_inicio',
        'fecha_entrega',
        'cliente',
        'matafuegos',
        'estados',
        'estado',
        'monto_total'
    )
<<<<<<< Updated upstream
    search_fields = ('id', 'cliente__codigo', 'fecha_creacion','matafuegos__id',)
    list_filter= ('estado',)
    inlines = [TareaTabularInline]
    readonly_fields = ['fecha_creacion', 'fecha_inicio','fecha_cierre', 'monto_total',]
=======
    model = Ordenes_de_trabajo
    list_filter=('estado',)
    search_fields = ('numero', 'cliente_codigo', 'fecha',)
    inlines = [TareaTabularInline]
>>>>>>> Stashed changes
    actions = [action_iniciada, action_finalizada]
    ordering=['-fecha_cierre']

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.estado == 'f':
            return ['numero', 'fecha', 'fecha_entrega', 'fecha_cierre','notas', 'cliente', 'estado', 'monto_total', 'matafuegos']
        else:
            return ['monto_total']


class TareaOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'tarea',
        'orden'
    )

admin.site.register(Ordenes_de_trabajo, OrdenTrabajoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Tarea_Orden, TareaOrdenAdmin)
