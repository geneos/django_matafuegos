from django.contrib import admin

# Register your models here.
from django.contrib.admin.helpers import ActionForm
from django import forms

from .models import Cliente, estados
from orden_trabajo.models import Ordenes_de_trabajo

from matafuegos.models import Matafuegos


@admin.action(description='Estado inactivo')
def make_inactivo(modeladmin, request, queryset):
    queryset.update(estado='i')

@admin.action(description='Estado activo')
def make_activo(modeladmin, request, queryset):
    queryset.update(estado='a')

class OrdenTrabajoTabularInline(admin.TabularInline):
    model = Ordenes_de_trabajo
    can_delete = False
    readonly_fields =  ('numero','fecha','fecha_entrega','fecha_cierre','cliente','estado','monto_total',)
    fields = ('numero','fecha','fecha_entrega','fecha_cierre','cliente','estado','monto_total',)
    def has_add_permission(self, request, obj=None):
        return False

class MatafuegoabularInline(admin.TabularInline):
    model = Matafuegos
    can_delete = False
    readonly_fields = ('numero', 'numero_dps', 'direccion', 'categoria', 'tipo',)
    fields = ('numero', 'numero_dps', 'direccion', 'categoria', 'tipo',)
    ordering = ('numero_dps',)
    def has_add_permission(self, request, obj=None):
        return False

class CLienteAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'cuit_cuil',
        'nombre',
        'direccion',
    )

    search_fields= ('codigo', 'nombre', 'cuit_cuil',)
    list_filter= ('estado', 'tipo',)
    actions = [make_inactivo, make_activo]
    inlines = [OrdenTrabajoTabularInline, MatafuegoabularInline]

admin.site.register(Cliente, CLienteAdmin)
