import os
from datetime import date, timedelta
from io import BytesIO
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import FileResponse
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reportlab.pdfgen import canvas
from .models import CategoriaMatafuegos, TipoMatafuegos, MarcaMatafuegos, Matafuegos
from .forms import ControlPatenteForm

class MatafuegosResource(resources.ModelResource):

    class Meta:
        model = Matafuegos

class MatafuegosAdmin(ImportExportModelAdmin):
    list_display = (
        'numero',
        'numeroInterno',
        'numero_dps',
        'fecha_proxima_carga',
        'fecha_proxima_ph',
    )
    form = ControlPatenteForm
    search_fields= ('cliente__nombre','numero', 'numero_dps',)
    list_filter= ('categoria',)
    actions = ['proximos_vencimientos','alerta_vencimientos']
    readonly_fields=['fecha_proxima_carga','fecha_proxima_ph']
    resource_class = MatafuegosResource


    """Funcion para que no sea necesario seleccionar un matafuego para la accion proximos-vencimientos"""
    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and (request.POST['action'] == 'proximos_vencimientos' or request.POST['action'] == 'alerta_vencimientos'):
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({ACTION_CHECKBOX_NAME: str(Matafuegos.objects.first().id)})
                request._set_post(post)
        return super(MatafuegosAdmin, self).changelist_view(request, extra_context)

    """Accion para emitir los vencimientos de carga y ph del proximo mes"""
    @admin.action(description="Informe proximos vencimientos")
    def proximos_vencimientos(self, request, obj):
        today = date.today()
        td = timedelta(30)
        filtroC = Matafuegos.objects.filter(fecha_proxima_carga__range=(today, today + td)).order_by('cliente')
        filtroPH = Matafuegos.objects.filter(fecha_proxima_ph__range=(today, today + td)).order_by('cliente')
        return self.emitirInforme(request,filtroC,filtroPH)

    """Escritura del informe de los proximos vencimientos"""
    def emitirInforme(self,request, carga,ph):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        settings_dir = os.path.dirname(__file__)
        PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
        img = os.path.join(PROJECT_ROOT, 'seguridad_fenix.png')
        pdf.drawImage(img, 22,720,550,100)
        y = 680
        x = 45
        e = 15
        if carga.count()<1 and ph.count()<1:
            return messages.error(request,'No hay matafuegos con vencimiento en los proximos 30 dias')
        else:
            pdf.setFont('Helvetica-Bold', 14)
            pdf.drawString(x, y, 'Carga de matafuegos')
            pdf.setFont("Helvetica", 10)
            y = y-18
            c = None
            for d in carga:
                if c != d.cliente:
                    y = y-18
                    c = d.cliente
                    pdf.drawString(x, y, 'Nombre/Razón Social: '+str(d.cliente))
                    y = y-15
                    pdf.drawString(x, y, 'Telefono: '+str(d.cliente.telefono))
                    y = y-e
                    pdf.drawString(x, y, 'Email: '+str(d.cliente.email))
                    y = y-e
                    xlist = [50, 173, 296, 419, 542]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    pdf.drawString(52, y-16, 'Numero')
                    pdf.drawString(175, y-16, 'Numero de DPS')
                    pdf.drawString(298, y-16, 'Fecha de vencimiento')
                    pdf.drawString(421, y-16, 'Direccion')
                    y=y-18
                xlist = [50, 173, 296, 419, 542]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(52, y-16, str(d.numero))
                pdf.drawString(175, y-16, str(d.numero_dps))
                pdf.drawString(298, y-16, str(d.fecha_proxima_carga))
                pdf.drawString(421, y-16, str(d.direccion))
                y = y-18
                if (y<50):
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = 800
                    x = 45
                    e = 15
                    xlist = [50, 173, 296, 419, 542]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    pdf.drawString(52, y-16, 'Numero')
                    pdf.drawString(175, y-16, 'Numero de DPS')
                    pdf.drawString(298, y-16, 'Fecha de vencimiento')
                    pdf.drawString(421, y-16, 'Direccion')
                    y=y-18
            y = y-38
            pdf.setFont('Helvetica-Bold', 14)
            pdf.drawString(x, y, 'PH de matafuegos')
            pdf.setFont("Helvetica", 10)
            y = y-18
            c = None
            for d in carga:
                if c != d.cliente:
                    y = y-18
                    c = d.cliente
                    pdf.drawString(x, y, 'Nombre/Razón Social: '+str(d.cliente))
                    y = y-15
                    pdf.drawString(x, y, 'Telefono: '+str(d.cliente.telefono))
                    y = y-e
                    pdf.drawString(x, y, 'Email: '+str(d.cliente.email))
                    y = y-e
                    xlist = [50, 173, 296, 419, 542]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    pdf.drawString(52, y-16, 'Numero')
                    pdf.drawString(175, y-16, 'Numero de DPS')
                    pdf.drawString(298, y-16, 'Fecha de vencimiento')
                    pdf.drawString(421, y-16, 'Direccion')
                    y=y-18
                xlist = [50, 173, 296, 419, 542]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(52, y-16, str(d.numero))
                pdf.drawString(175, y-16, str(d.numero_dps))
                pdf.drawString(298, y-16, str(d.fecha_proxima_ph))
                pdf.drawString(421, y-16, str(d.direccion))
                y = y-18
                if (y<50):
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = 800
                    x = 45
                    e = 15
                    xlist = [50, 173, 296, 419, 542]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    pdf.drawString(52, y-16, 'Numero')
                    pdf.drawString(175, y-16, 'Numero de DPS')
                    pdf.drawString(298, y-16, 'Fecha de vencimiento')
                    pdf.drawString(421, y-16, 'Direccion')
                    y=y-18
            pdf.showPage()
            pdf.save()
            buffer.seek(0)
            messages.success(request, "Informe emitido")
            return FileResponse(buffer, as_attachment=True, filename='proximos_vencimientos.pdf')

    #----------------------------------------------------------------------------------------------


    """Accion para emitir los vencimientos de carga y ph del proximo mes"""
    @admin.action(description="Alerta de vencimientos")
    def alerta_vencimientos(self, request, obj):
        today = date.today()
        td = timedelta(30)
        filtroC = Matafuegos.objects.filter(fecha_proxima_carga__range=(today, today + td)).order_by('cliente')
        filtroPH = Matafuegos.objects.filter(fecha_proxima_ph__range=(today, today + td)).order_by('cliente')
        lista = list(set(filtroC) | set(filtroPH))
        return self.emitirAlerta(request,lista)

    """Escritura del informe alerta de los proximos vencimientos"""
    def emitirAlerta(self,request,lista):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        settings_dir = os.path.dirname(__file__)
        PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
        img = os.path.join(PROJECT_ROOT, 'seguridad_fenix.png')
        pdf.drawImage(img, 22,720,550,100)
        y = 680
        x = 45
        if len(lista) < 1:
            return messages.error(request,'No hay matafuegos con vencimiento en los proximos 30 dias')
        else:
            pdf.setFont('Helvetica-Bold', 14)
            pdf.drawString(x, y, 'Vencimientos de matafuegos')
            pdf.setFont("Helvetica-Bold", 10)
            y = y-18
            xlist = [30, 140, 186,293,334,382,445,505, 565]
            ylist = [y, y-18]
            pdf.grid(xlist, ylist)
            pdf.drawString(32, y-16, 'Cliente')
            pdf.drawString(142, y-16, '# Ubic')
            pdf.drawString(188, y-16, 'Ubicacion')
            pdf.drawString(295, y-16, 'Tipo')
            pdf.drawString(336, y-16, 'Volumen')
            pdf.drawString(384, y-16, 'Matafuego')
            pdf.drawString(447, y-16, 'Venc carga')
            pdf.drawString(507, y-16, 'Venc ph')
            y=y-18
            pdf.setFont("Helvetica", 9)
            for d in lista:
                xlist = [30, 140, 186,293,334,382,445,505, 565]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                if len(d.cliente.nombre)>20:
                    pdf.drawString(32, y-16, d.cliente.nombre[0:19])
                else:
                    pdf.drawString(32, y-16, d.cliente.nombre)
                if d.numero_localizacion:
                    pdf.drawString(142, y-16, str(d.numero_localizacion))
                if d.localizacion != "NULL":
                    if len(d.localizacion)>18:
                        pdf.drawString(188, y-16, d.localizacion[0:17])
                    else:
                        pdf.drawString(188, y-16, d.localizacion)
                pdf.drawString(295, y-16, d.tipo.tipo)
                pdf.drawString(336, y-16, str(d.tipo.volumen))
                pdf.drawString(384, y-16, str(d.numero))
                pdf.drawString(447, y-16, str(d.fecha_proxima_carga))
                pdf.drawString(507, y-16, str(d.fecha_proxima_ph))
                y = y-18
                if (y<50):
                    pdf.showPage()
                    pdf.setFont("Helvetica-Bold", 10)
                    y = 800
                    xlist = [30, 140, 186,293,334,382,445,505, 565]
                    ylist = [y, y-18]
                    pdf.grid(xlist, ylist)
                    pdf.drawString(32, y-16, 'Cliente')
                    pdf.drawString(142, y-16, '# Ubic')
                    pdf.drawString(188, y-16, 'Ubicacion')
                    pdf.drawString(295, y-16, 'Tipo')
                    pdf.drawString(336, y-16, 'Volumen')
                    pdf.drawString(384, y-16, 'Matafuego')
                    pdf.drawString(447, y-16, 'Venc carga')
                    pdf.drawString(507, y-16, 'Venc ph')
                    y=y-18
                    pdf.setFont("Helvetica", 9)
            pdf.showPage()
            pdf.save()
            buffer.seek(0)
            messages.success(request, "Informe emitido")
            return FileResponse(buffer, as_attachment=True, filename='alerta_vencimientos.pdf')
class TipoMatafuegosAdmin(admin.ModelAdmin):
    list_display = (
        'tipo',
        'categoria',
        'vencimiento_carga',
        'vencimiento_ph',
        'volumen',
        'peso',
    )
    search_fields= ('tipo',)
    list_filter= ('categoria',)

admin.site.register(CategoriaMatafuegos)
admin.site.register(TipoMatafuegos, TipoMatafuegosAdmin)
admin.site.register(MarcaMatafuegos)
admin.site.register(Matafuegos, MatafuegosAdmin)
