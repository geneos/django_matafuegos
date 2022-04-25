from django.contrib import admin

# Register your models here.
from django.contrib.admin.helpers import ActionForm
from django import forms

from .models import Cliente, estados

@admin.action(description='Estado inactivo')
def make_inactivo(modeladmin, request, queryset):
    queryset.update(estado='i')

@admin.action(description='Estado activo')
def make_activo(modeladmin, request, queryset):
    queryset.update(estado='a')

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


admin.site.register(Cliente, CLienteAdmin)
