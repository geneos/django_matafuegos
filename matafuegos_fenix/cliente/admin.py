<<<<<<< Updated upstream
import os
from io import BytesIO
from django.contrib import admin, messages
from django.http import FileResponse
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from .models import Cliente, estados
from orden_trabajo.models import Ordenes_de_trabajo,TareaOrden
from matafuegos.models import Matafuegos

#ACCIONES
=======
from django.contrib import admin

# Register your models here.
import os
from django.contrib import admin, messages
from django.http import FileResponse
from io import BytesIO
from .models import Cliente
from reportlab.pdfgen import canvas
from orden_trabajo.models import Ordenes_de_trabajo
from matafuegos.models import Matafuegos

@admin.action(description="Informe del cliente")
def emitirInformeCliente(self, request, queryset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    set = queryset.all()
    y = 700
    x = 45
    e = 15
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'seguridad_fenix.png')
    pdf.drawImage(img, 22,720,550,100)
    pdf.setFont("Helvetica", 10)
    if set.count()>1:
        return messages.error(request,'Debe seleccionar solo un cliente')
    else:
        for d in set:
            pdf.drawString(x, y, 'Nombre/Razón Social: '+str(d.nombre))
            y = y-15
            pdf.drawString(x, y, 'Codigo: '+str(d.codigo))
            y = y-e
            pdf.drawString(x, y, 'CUIT/CUIL: '+str(d.cuit_cuil))
            y = y-e
            pdf.drawString(x, y, 'Dirección: '+str(d.direccion))
            y = y-e
            pdf.drawString(x, y, 'Telefono: '+str(d.telefono))
            y = y-e
            pdf.drawString(x, y, 'Email: '+str(d.email))
            y = y-e
            pdf.drawString(x, y, 'Web: '+str(d.web))
            y = y-e
            pdf.drawString(x, y, 'Tipo: '+str(d.tipo))
            y = y-e
            pdf.drawString(x, y, 'Estado: '+str(d.estado))
            y = y-30
            pdf.setFont('Helvetica-Bold', 14)
            pdf.drawString(x, y, 'Matafuegos')
            pdf.setFont("Helvetica", 10)
            y = y-10
            matafuegos = Matafuegos.objects.filter(cliente = d.id)
            xlist = [50,132 , 217, 329, 381, 463,545]
            ylist = [y, y-18]
            pdf.drawString(53, y-16, 'Numero')
            pdf.drawString(135, y-16, 'Numero de DPS')
            pdf.drawString(220, y-16, 'Localizacion')
            pdf.drawString(332, y-16, 'Tipo')
            pdf.drawString(383, y-16, 'Fecha prox carga')
            pdf.drawString(466, y-16, 'Fecha prox PH')
            pdf.grid(xlist, ylist)
            y = y-18
            for m in matafuegos:
                xlist = [50,132 , 217, 329, 381, 463,545]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(53, y-16, str(m.numero))
                pdf.drawString(135, y-16,str(m.numero_dps))
                pdf.drawString(220, y-16,str(m.direccion))
                pdf.drawString(332, y-16,str(m.tipo))
                pdf.drawString(383, y-16,str(m.fecha_proxima_carga))
                pdf.drawString(466, y-16,str(m.fecha_proxima_ph))
                y = y-18
                if (y<50):
                    y = 800
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    xlist = [50,132 , 217, 329, 381, 463,545]
                    ylist = [y, y-18]
                    pdf.drawString(53, y-16, 'Numero')
                    pdf.drawString(135, y-16, 'Numero de DPS')
                    pdf.drawString(220, y-16, 'Localizacion')
                    pdf.drawString(332, y-16, 'Tipo')
                    pdf.drawString(383, y-16, 'Fecha prox carga')
                    pdf.drawString(466, y-16, 'Fecha prox PH')
                    pdf.grid(xlist, ylist)
                    y = y-18
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


>>>>>>> Stashed changes
@admin.action(description='Estado inactivo')
def make_inactivo(modeladmin, request, queryset):
    queryset.update(estado='i')

@admin.action(description='Estado activo')
def make_activo(modeladmin, request, queryset):
    queryset.update(estado='a')


<<<<<<< Updated upstream
def cabeceraTablaMatafuegos(pdf,y):
    pdf.setFont("Helvetica-Bold", 10)
    xlist = [45, 132, 217, 329, 381, 468, 560]
    ylist = [y, y-22]
    pdf.drawString(47, y-16, 'Numero')
    pdf.drawString(135, y-16, 'Numero de DPS')
    pdf.drawString(220, y-16, 'Localizacion')
    pdf.drawString(332, y-16, 'Tipo')
    pdf.drawString(383, y-16, 'Fecha prox carga')
    pdf.drawString(470, y-16, 'Fecha prox PH')
    pdf.grid(xlist, ylist)

def cabeceraTablaOrdenes(pdf,y):
    pdf.setFont("Helvetica-Bold", 10)
    xlist = [45,124 , 183,250, 320,387,450, 560]
    ylist = [y, y-22]
    pdf.grid(xlist, ylist)
    pdf.drawString(47, y-16, 'Numero Orden')
    pdf.drawString(126, y-16, 'Matafuegos')
    pdf.drawString(185, y-16, 'Fecha inicio')
    pdf.drawString(252, y-16, 'Fecha cierre')
    pdf.drawString(322, y-16, 'Estado')
    pdf.drawString(389, y-16, 'Monto Total')
    pdf.drawString(452, y-16, 'Tareas realizadas')



#Emite el informe con la informacion de un cliente, los matafuegos que tiene asociado y las tareas.
@admin.action(description="Informe del cliente")
def emitirInformeCliente(self, request, queryset):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    img = os.path.join(PROJECT_ROOT, 'seguridad_fenix.png')
    pdf.drawImage(img, 22,720,550,100)
    set = queryset.all()
    y = 700
    x = 45
    e = 15
    pdf.setFont("Helvetica", 12)
    pdf.drawString(x, y, 'INFORME DEL CLIENTE')
    pdf.setFont("Helvetica", 10)
    y= y-15
    if set.count()>1:
        return messages.error(request,'Debe seleccionar solo un cliente')
    else:
        for d in set:
            pdf.drawString(x, y, 'Nombre/Razón Social: '+str(d.nombre))
            y = y-15
            pdf.drawString(x, y, 'Codigo: '+str(d.codigo))
            y = y-e
            pdf.drawString(x, y, 'CUIT/CUIL: '+str(d.cuit_cuil))
            y = y-e
            pdf.drawString(x, y, 'Dirección: '+str(d.direccion))
            y = y-e
            pdf.drawString(x, y, 'Telefono: '+str(d.telefono))
            y = y-e
            y = y-30
            pdf.drawString(x, y, 'MATAFUEGOS')
            y = y-10
            matafuegos = Matafuegos.objects.filter(cliente = d.id)
            cabeceraTablaMatafuegos(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-22
            for m in matafuegos:
                xlist = [45,132 , 217, 329, 381, 468,560]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(48, y-16, str(m.numero))
                pdf.drawString(135, y-16,str(m.numero_dps))
                pdf.drawString(220, y-16,str(m.direccion))
                pdf.drawString(332, y-16,str(m.tipo))
                pdf.drawString(383, y-16,str(m.fecha_proxima_carga))
                pdf.drawString(470, y-16,str(m.fecha_proxima_ph))
                y = y-18
                if (y<50):
                    y = 800
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    cabeceraTablaMatafuegos(pdf,y)
                    pdf.setFont("Helvetica", 10)
                    y = y-18
            pdf.drawString(45, y-25, 'ORDENES DE TRABAJO')
            y= y - 30
            ordenes= Ordenes_de_trabajo.objects.filter(cliente= d.id)
            cabeceraTablaOrdenes(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-22
            for o in ordenes:
                xlist = [45, 124, 183, 250, 320, 387, 450, 560]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                inicio = y
                pdf.drawString(48, y-16, str(o.id))
                pdf.drawString(126, y-16, str(o.matafuegos))
                pdf.drawString(185, y-16, str(o.fecha_inicio))
                pdf.drawString(252, y-16, str(o.fecha_cierre))
                if str(o.estado) == 'f':
                    pdf.drawString(322, y-16, "Finalizada")
                elif str(o.estado) == 'c':
                    pdf.drawString(322, y-16, " Cancelada")
                elif str(o.estado) == 'p':
                    pdf.drawString(322, y-16, " Pendiente")
                elif str(o.estado) == 'ep':
                    pdf.drawString(322, y-16, "En proceso")
                pdf.drawString(389, y-16,str(o.monto_total))
                tareas= TareaOrden.objects.filter(orden= o.id)
                for t in tareas:
                    xlist = [45, 124, 183, 250, 320, 387, 450, 560]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    nombre= str(t.tarea.nombre)
                    if len(nombre)>25:
                        nombre= nombre[0:25]
                    pdf.drawString(452, y-16, str(nombre))
                    y=y-18
                    if (y<50):
                        y = 800
                        pdf.showPage()
                        cabeceraTablaOrdenes(pdf,y)
                        pdf.setFont("Helvetica", 10)
                        y = y-22
                if (y<50):
                    y = 800
                    pdf.showPage()
                    cabeceraTablaOrdenes(pdf,y)
                    pdf.setFont("Helvetica", 10)
                    y = y-22
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')

=======
>>>>>>> Stashed changes
class OrdenTrabajoTabularInline(admin.TabularInline):
    model = Ordenes_de_trabajo
    can_delete = False
    fields = ('fecha_creacion','fecha_inicio','fecha_entrega','fecha_cierre','cliente','estado','monto_total',)
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

class MatafuegoTabularInline(admin.TabularInline):
    model = Matafuegos
    can_delete = False
    fields = ('numero', 'numero_dps', 'direccion', 'categoria', 'tipo',)
    ordering = ('numero_dps',)
    def has_change_permission(self, request, obj=None):
        return False
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
    actions = [make_inactivo, make_activo, emitirInformeCliente]
    inlines = [OrdenTrabajoTabularInline, MatafuegoTabularInline]

admin.site.register(Cliente, CLienteAdmin)
