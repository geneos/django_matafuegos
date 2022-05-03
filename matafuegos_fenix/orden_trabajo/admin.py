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
    queryset.update(fecha_inicio=date.today())
    queryset.update(fecha_cierre=None)

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
        'estado',
        'monto_total'
    )
    search_fields = ('id', 'cliente__codigo', 'fecha_creacion','matafuegos__id',)
    list_filter= ('estado',)
    inlines = [TareaTabularInline]
    readonly_fields = ['fecha_creacion', 'fecha_inicio','fecha_cierre', 'monto_total',]
    actions = [action_iniciada, action_finalizada]

class TareaOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'tarea',
        'orden'
    )

admin.site.register(Ordenes_de_trabajo, OrdenTrabajoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Tarea_Orden, TareaOrdenAdmin)
