from django.contrib import admin

# Register your models here.
from django.contrib.admin.helpers import ActionForm
from django import forms

from .models import Cliente, estados
from orden_trabajo.models import Ordenes_de_trabajo


@admin.action(description='Estado inactivo')
def make_inactivo(modeladmin, request, queryset):
    queryset.update(estado='i')

@admin.action(description='Estado activo')
def make_activo(modeladmin, request, queryset):
    queryset.update(estado='a')

class OrdenTrabajoTabularInline(admin.TabularInline):
    model = Ordenes_de_trabajo
    can_delete = True

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
    inlines = [OrdenTrabajoTabularInline]


admin.site.register(Cliente, CLienteAdmin)
