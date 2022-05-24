import os
from datetime import date
from io import BytesIO
from django.contrib import admin, messages
from django.http import FileResponse
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from .forms import OrdenForm
from .models import Tarea, Ordenes_de_trabajo, TareaOrden


class TareaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'precio',
    )

class TareaTabularInline(admin.TabularInline):
    model = TareaOrden
    can_delete = True
    fields = ('tarea', 'precioAj')

#ACCIONES
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

#Accion para que emita el informe de toda la informacion y las tareas de la orden seleccionada
@admin.action(description="Informe Ordenes de trabajo")
def emitirInformeOrden(self, request, queryset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'seguridad_fenix.png')
    pdf.drawImage(img, 22,720,550,100)
    y= 700
    x=50
    set = queryset.all()
    if set.count() == 1:
        d= set[0]
        pdf.setFont("Helvetica", 14)
        pdf.drawString(x, y-10, str("INFORME DE LA ORDEN DE TRABAJO"))
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y-25, "Numero de orden: " + str(d.id))
        pdf.drawString(x, y-40, "Fecha inicio de orden: " + str(d.fecha_inicio))
        pdf.drawString(x, y-55, "Fecha cierre de orden: " + str(d.fecha_cierre))
        pdf.drawString(x, y-70, "Cliente: " + str(d.cliente))
        pdf.drawString(x, y-85, "Matafuego: " + str(d.matafuegos))
        if str(d.estado) == 'f':
            pdf.drawString(x, y-100, "Estado de la orden: Finalizada")
        elif str(d.estado) == 'c':
            pdf.drawString(x, y-100, "Estado de la orden: Cancelada")
        elif str(d.estado) == 'p':
            pdf.drawString(x, y-100, "Estado de la orden: Pendiente")
        elif str(d.estado) == 'ep':
            pdf.drawString(x, y-100, "Estado de la orden: En proceso")
        tareas = TareaOrden.objects.filter(orden = d.id)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(x, y-135, str("TAREAS REALIZADAS"))
        pdf.setFont("Helvetica", 12)
        xlist = [x, x+400, x+500]
        ylist =[y-140, y-156]
        pdf.grid(xlist, ylist)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x+5, y-154, "Nombre de la tarea")
        pdf.drawString(x+403, y-154, "Precio")
        pdf.setFont("Helvetica", 12)
        y=y-156
        for t in tareas:
            xlist = [x, x+400, x+500]
            ylist =[y, y-16]
            nombre= str(t.tarea.nombre)
            if len(nombre)>75:
                nombre= nombre[0:75]
            pdf.drawString(x+3, y-14, str(nombre))
            pdf.drawString(x+403, y-14, str(t.tarea.precio))
            pdf.grid(xlist, ylist)
            y-=16
            if (y<50):
                y = 800
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                xlist = [x, x+400, x+500]
                ylist =[y, y-16]
                pdf.grid(xlist, ylist)
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(x+5, y-14, "Nombre de la tarea")
                pdf.drawString(x+403, y-14, "Precio")
                pdf.setFont("Helvetica", 12)
                y=y-16
        xlist = [x, x+400, x+500]
        ylist =[y, y-16]
        pdf.grid(xlist, ylist)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(x, y-14, " Monto total: ")
        pdf.drawString(x+402, y-14,str(d.monto_total))
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='informe de orden.pdf')
    else:
        messages.error(request, "Seleccionar una orden")

#Accion para que emita la información de las DPS domiciliarias
@admin.action(description="Informe DPS Domiciliaria")
def emitirInformeDPSFijo(self, request, queryset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    y= 752
    x=50
    pdf.setFont("Helvetica", 10)
   #pdf.drawImage("DPS FIJA 2019.png", 0, 40, width=595, height=800)
    set = queryset.all()
    cant= set.count()
    if set.count() % 3 == 0:
        for d in set:
            cant-=1
            if str(d.matafuegos.categoria) == 'd':
                pdf.drawString(x, y, str(d.matafuegos.numero))#NUMERO DE MATAFUEGO
                pdf.drawString(x+67, y, str(d.matafuegos.fecha_fabricacion.year))# AÑO FABRICACIÓN
                pdf.drawString(x, y-20, str("SEGURIDAD FENIX SA"))
                pdf.drawString(x, y-20, str("SEGURIDAD FENIX SA"))
                pdf.drawString(x+125, y-20, str("120"))
                pdf.drawString(x+101, y,str(d.matafuegos.fecha_proxima_ph.month)+" "+str(d.matafuegos.fecha_proxima_ph.year))
                pdf.drawString(x+140, y,str(d.matafuegos.tipo.volumen))#CAPACIDAD
                pdf.drawString(x+170, y,str(d.matafuegos.tipo)) #AGENTE EXTINTOR
                # ______________
                pdf.drawString(x+8, y-55,str(d.matafuegos.fecha_proxima_carga.month)) #Proxima revision recarga mes
                pdf.drawString(x+35, y-55,str(d.matafuegos.fecha_proxima_carga.year)) #Proxima revision recarga año
                #Para exintor
                pdf.drawString(x+240, y-21, str(d.matafuegos.numero))#NUMERO DE MATAFUEGO
                pdf.drawString(x+290, y-21, str(d.matafuegos.fecha_proxima_ph.month)+ ' ' +str(d.matafuegos.fecha_proxima_ph.year ))#venc PH
                pdf.drawString(x+243, y-58,str(d.matafuegos.fecha_proxima_carga.month))
                pdf.drawString(x+269, y-58,str(d.matafuegos.fecha_proxima_carga.year))
                y = y-288
            else:
                messages.error(request, "Seleccionar solo categoria domiciliaria")
                return
            if (cant % 3 == 0 and cant !=0):
                    y = 752
                    pdf.showPage()
                    pdf.drawImage("DPS FIJA 2019.png", 0, 40, width=595, height=800)
                    pdf.setFont("Helvetica", 10)
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='DPS FIJA.pdf')
    else:
        messages.error(request, "Seleccionar multiplos de 3")


class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha_inicio',
        'fecha_entrega',
        'cliente',
        'matafuegos',
        'get_categoria',
        'estados',
        'estado',
        'monto_total'

    )

    def get_categoria(self, obj):
        if obj.matafuegos.categoria == 'd':
            return 'Domiciliaria'
        return 'Vehicular'
    get_categoria.short_description = 'Categoria'
    search_fields = ('id', 'cliente__codigo', 'fecha_creacion','matafuegos__id',)
    list_filter = ('estado', 'matafuegos__categoria',)
    inlines = [TareaTabularInline]
    readonly_fields = ['fecha_creacion', 'fecha_inicio','fecha_cierre','monto_total','estados',]
    model = Ordenes_de_trabajo
    actions = [action_iniciada, action_finalizada,emitirInformeDPSFijo, emitirInformeOrden]
    ordering = ['-fecha_cierre']

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and (obj.estado == 'f' or obj.estado == 'c'):
            return ['id','fecha_inicio', 'fecha_entrega','fecha_creacion', 'fecha_cierre','notas', 'cliente', 'estado', 'monto_total', 'matafuegos']
        else:
            return ['estado','fecha_creacion', 'fecha_inicio', 'fecha_cierre','monto_total', ]


class TareaOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'tarea',
        'orden'
    )

admin.site.register(Ordenes_de_trabajo, OrdenTrabajoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(TareaOrden, TareaOrdenAdmin)
