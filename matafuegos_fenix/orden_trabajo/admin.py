import os
from datetime import date, timedelta
from io import BytesIO
from urllib import request

from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib import admin, messages
from reportlab.lib.units import inch
from .forms import OrdenesTrabajoAdminForm
from .models import Tarea, Ordenes_de_trabajo, TareaOrden, Matafuegos
from parametros.models import Parametros



class TareaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'precio',
    )

class TareaTabularInline(admin.TabularInline):
    model = TareaOrden
    can_delete = True
    fields = ('tarea', 'cant_cargada')

class TareaFinalizadaTabularInline(admin.TabularInline):
    model = TareaOrden
    can_delete = True
    fields = ('tarea',)
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

#ACCIONES

#Accion para iniciar la orden y pasar de estado pendiente a en proceso. -No usada por ahora porque ya inicia en 'En proceso'
@admin.action(description='Iniciar orden de trabajo')
def action_iniciada(modeladmin, request, queryset):
    queryset.update(estado='ep')
    queryset.update(fecha_inicio=date.today())
    queryset.update(fecha_cierre=None)

# Accion para finalizar la ornden y pasar a estado finalizada
@admin.action(description='Finalizar orden de trabajo')
def action_finalizada(modeladmin, request, queryset):
    queryset.update(estado='f')
    queryset.update(fecha_cierre=date.today())

@admin.action(description='Cancelar orden de trabajo')
def action_cancelada(modeladmin, request, queryset):
    queryset.update(estado='c')

@admin.action(description="Oblea DPS vehicular")
def emitirInformeVehicular(self, request, queryset):
    # Create file to recieve data and create the PDF
    buffer = BytesIO()
    # Create the file PDF
    pdf = canvas.Canvas(buffer)
    pdf.setPageSize((6.69291*inch, 12*inch))
    # Inserting in PDF where this 2 first arguments are axis X and Y respectvely
    set = queryset.all()
    y = 773
    x = 50
    pdf.setFont("Helvetica", 10)
    cant = set.count()
    if set.count() % 3 != 0:
        return messages.error(request,'La cantidad de ordenes de trabajo debe ser multiplo de tres')
    else:
        for d in set:
            if d.matafuegos.categoria != 'v' and d.matafuegos.categoria != 'ma':
                return messages.error(request,'Deben ser ordenes de trabajo de matafuegos vehiculares o de maquinarias agricolas')
        for d in set:
            pdf.drawString(x+3, y, str(d.matafuegos.numero))
            pdf.drawString(x+71, y,str(d.matafuegos.fecha_fabricacion.year))
            pdf.drawString(x+110, y,str(d.matafuegos.fecha_proxima_ph.month)+" "+str(d.matafuegos.fecha_proxima_ph.year))
            pdf.drawString(x+145, y,str(d.matafuegos.tipo.volumen))
            pdf.drawString(x+176, y,str(d.matafuegos.categoria))
            pdf.drawString(x+3, y-23, str("SEGURIDAD FENIX SA"))
            pdf.drawString(x+128, y-23, str("120"))
            pdf.drawString(x+252, y-23, str(d.matafuegos.numero))
            pdf.drawString(x+307, y-23,str(d.matafuegos.fecha_proxima_ph.month)+" "+str(d.matafuegos.fecha_proxima_ph.year))
            pdf.drawString(x+8, y-60,str(d.matafuegos.fecha_proxima_carga.month))
            pdf.drawString(x+35, y-60,str(d.matafuegos.fecha_proxima_carga.year))
            pdf.drawString(x+163, y-60,str(d.matafuegos.patente))
            pdf.drawString(x+250, y-60,str(d.matafuegos.fecha_proxima_carga.month))
            pdf.drawString(x+278, y-60,str(d.matafuegos.fecha_proxima_carga.year))
            pdf.drawString(x+325, y-60,str(d.matafuegos.patente))
            y = y-295
            cant -=1
            Matafuegos.objects.filter(id = d.matafuegos.id).update(numero_dps = Parametros.objects.first().veh_actual)
            Parametros.objects.filter(id = Parametros.objects.first().id).update(veh_actual = Parametros.objects.first().veh_actual+2)
            if cant % 3 == 0 and cant !=0:
                y = 750
                x = 50
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
        pdf.save()
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='oblea_DPS_vehicular.pdf')




#Accion para que emita la información de las DPS domiciliarias
@admin.action(description="Oblea DPS Domiciliaria")
def emitirInformeDPSFijo(self, request, queryset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setPageSize((6.69291*inch, 12*inch))
    y= 775
    x=52
    pdf.setFont("Helvetica", 10)
    set = queryset.all()
    cant= set.count()
    if set.count() % 3 == 0:
        for d in set:
            cant-=1
            if str(d.matafuegos.categoria) == 'd':
                d.impresa=1
                d.save()
                pdf.drawString(x, y, str(d.matafuegos.numero))#NUMERO DE MATAFUEGO
                pdf.drawString(x+67, y, str(d.matafuegos.fecha_fabricacion.year))# AÑO FABRICACIÓN
                pdf.drawString(x, y-24, str("SEGURIDAD FENIX SA"))
                pdf.drawString(x, y-24, str("SEGURIDAD FENIX SA"))
                pdf.drawString(x+125, y-24, str("120"))
                pdf.drawString(x+106, y,str(d.matafuegos.fecha_proxima_ph.month)+" "+str(d.matafuegos.fecha_proxima_ph.year))
                pdf.drawString(x+141, y,str(d.matafuegos.tipo.volumen))#CAPACIDAD
                pdf.drawString(x+173, y,str(d.matafuegos.tipo)) #AGENTE EXTINTOR
                # ______________
                pdf.drawString(x+8, y-59,str(d.matafuegos.fecha_proxima_carga.month)) #Proxima revision recarga mes
                pdf.drawString(x+36, y-59,str(d.matafuegos.fecha_proxima_carga.year)) #Proxima revision recarga año
                nombre=str(d.matafuegos.cliente.nombre)#Nombre usuario
                if len(nombre)>11:
                    pdf.drawString(x+77, y-54,nombre[0:11])
                    pdf.drawString(x+77, y-64, nombre[12:])
                else:
                    pdf.drawString(x+77, y-54, nombre)
                #Para exintor
                pdf.drawString(x+244, y-24, str(d.matafuegos.numero))#NUMERO DE MATAFUEGO
                pdf.drawString(x+302, y-24, str(d.matafuegos.fecha_proxima_ph.month)+ ' ' +str(d.matafuegos.fecha_proxima_ph.year ))#venc PH
                pdf.drawString(x+248, y-59,str(d.matafuegos.fecha_proxima_carga.month))
                pdf.drawString(x+276, y-59,str(d.matafuegos.fecha_proxima_carga.year))
                y = y-296
                Matafuegos.objects.filter(id = d.matafuegos.id).update(numero_dps = Parametros.objects.first().dom_actual)
                Parametros.objects.filter(id = Parametros.objects.first().id).update(dom_actual = Parametros.objects.first().dom_actual+2)
            else:
                messages.error(request, "Seleccionar solo categoria domiciliaria")
                return
            if (cant % 3 == 0 and cant !=0):
                    y = 752
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='oblea_DPS_domiciliaria.pdf')
    else:
        messages.error(request, "Seleccionar multiplos de 3")

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

#Informe de las ordenes por cliente para la facturacion
def InformeFacturacion(request, ordenes):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'seguridad_fenix.png')
    pdf.drawImage(img, 22,720,550,100)
    y= 700
    x=50
    if ordenes.count()<1:
            return messages.error(request,'No hay ordenes finalizadas durante la ultima semana')
    else:
            pdf.setFont('Helvetica-Bold', 14)
            today = date.today()
            pdf.drawString(x, y, 'Informe facturacion ultima semana')
            y=y-15
            pdf.drawString(x, y, 'fecha: '+ str(today))
            pdf.setFont("Helvetica", 10)
            c = None
            for d in ordenes:
                tareas = TareaOrden.objects.filter(orden = d.id)
                if tareas.count()>0:
                    if c != d.cliente:
                        y = y-18
                        c = d.cliente
                        xlist = [50, 200, 232, 307, 367, 490, 542]
                        ylist = [y, y-18]
                        pdf.grid(xlist, ylist)
                        pdf.drawString(52, y-16, 'Cliente')
                        pdf.drawString(202, y-16, 'Orden')
                        pdf.drawString(234, y-16, 'Matafuego')
                        pdf.drawString(309, y-16, 'Fecha cierre')
                        pdf.drawString(369, y-16, 'Tarea')
                        pdf.drawString(492, y-16, 'Cantidad')
                        y=y-18
                    xlist = [50, 200, 232, 307, 367, 490, 542]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    nombre= str(d.cliente)
                    if len(nombre)>25:
                        nombre= nombre[0:24]
                    pdf.drawString(52, y-16, nombre)
                    pdf.drawString(204, y-16, str(d.id))
                    matafuegos= str(d.matafuegos)
                    if len(matafuegos)>12:
                        matafuegos= matafuegos[0:12]
                    pdf.drawString(234, y-16, matafuegos)
                    pdf.drawString(311, y-16, str(d.fecha_cierre.month) + " / "+ str(d.fecha_cierre.day))
                    t=0
                    tarea= str(tareas[t].tarea.nombre)
                    if len(tarea)>25:
                            tarea= tarea[0:24]
                    pdf.drawString(369, y-16, tarea )
                    pdf.drawString(492, y-16, str(tareas[t].cant_cargada))
                    y = y-18
                    t=1
                    while t < tareas.count():
                        xlist = [50,367, 490, 542]
                        ylist = [y, y-18]
                        pdf.grid(xlist, ylist)
                        tarea= str(tareas[t].tarea.nombre)
                        if len(tarea)>25:
                            tarea= tarea[0:24]
                        pdf.drawString(369, y-16, tarea )
                        pdf.drawString(492, y-16, str(tareas[t].cant_cargada))
                        t=t +1
                        y=y-18
                        if (y<50):
                            pdf.showPage()
                            pdf.setFont("Helvetica", 10)
                            y = 800
                            x = 45
                            e = 15
                            xlist = [50,367, 490, 542]
                            ylist = [y, y-18]
                            pdf.grid(xlist, ylist)

                    print(y)
                    if (y<10):
                        pdf.showPage()
                        pdf.setFont("Helvetica", 10)
                        y = 800
                        x = 45
                        e = 15
                        xlist = [50, 200, 232, 307, 367, 490, 542]
                        ylist = [y, y-18]
                        pdf.grid(xlist, ylist)
                        pdf.drawString(52, y-16, 'Cliente')
                        pdf.drawString(202, y-16, 'Orden')
                        pdf.drawString(234, y-16, 'Matafuego')
                        pdf.drawString(309, y-16, 'Fecha cierre')
                        pdf.drawString(369, y-16, 'Tarea')
                        pdf.drawString(492, y-16, 'Cantidad')
                        y=y-18
            pdf.showPage()
            pdf.save()
            buffer.seek(0)
            messages.success(request, "Informe emitido")
            return FileResponse(buffer, as_attachment=True, filename='informe_facturacion.pdf')

class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'matafuegos',
        'get_categoria',
        'estados',
        'estado',
        'impresa'

    )

    def get_categoria(self, obj):
        if obj.matafuegos.categoria == 'd':
            return 'Domiciliaria'
        return 'Vehicular'
    get_categoria.short_description = 'Categoria'
    autocomplete_fields = ('cliente',)
    search_fields = ('id', 'cliente__codigo', 'fecha_creacion','matafuegos__id',)
    list_filter = ('estado', 'matafuegos__categoria', 'impresa',)
    inlines = [TareaTabularInline]
    model = Ordenes_de_trabajo
    actions = [action_finalizada,emitirInformeDPSFijo, emitirInformeOrden,emitirInformeVehicular,'Informe_facturacion']
    ordering = ['-fecha_cierre']
    form = OrdenesTrabajoAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and (obj.estado == 'f' or obj.estado == 'c'):
            OrdenTrabajoAdmin.inlines = [TareaFinalizadaTabularInline]
            return ['id', 'fecha_inicio', 'fecha_entrega', 'fecha_creacion','fecha_cierre','notas', 'estado', 'monto_total', 'matafuegos','cliente']
        else:
            OrdenTrabajoAdmin.inlines = [TareaTabularInline]
            return ['fecha_creacion', 'fecha_inicio','fecha_cierre','monto_total','estado']

    """Funcion para que no sea necesario seleccionar una para el informe de facturacion"""
    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and (request.POST['action'] == 'Informe_facturacion'):
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({ACTION_CHECKBOX_NAME: str(Ordenes_de_trabajo.objects.first().id)})
                request._set_post(post)
        return super(OrdenTrabajoAdmin, self).changelist_view(request, extra_context)

    @admin.action(description="Informe Facturacion ultima semana")
    def Informe_facturacion(self, request, obj):
        today = date.today()
        td = timedelta(7)
        ordenes = Ordenes_de_trabajo.objects.filter(estado= 'f', fecha_cierre__range=(today - td, today)).order_by('cliente')
        return InformeFacturacion(request,ordenes)


class TareaOrdenAdmin(admin.ModelAdmin):
    list_display = (
        'tarea',
        'orden'
    )

admin.site.register(Ordenes_de_trabajo, OrdenTrabajoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(TareaOrden, TareaOrdenAdmin)
