from django.contrib import admin

# Register your models here.
from .models import Tarea, Ordenes_de_trabajo


class TareaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )

class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        #"'cliente',
    )

admin.site.register(Ordenes_de_trabajo, OrdenTrabajoAdmin)
admin.site.register(Tarea, TareaAdmin)
