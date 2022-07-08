import os
import smtplib
from datetime import date, timedelta
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import admin, messages
from django.http import FileResponse, HttpResponse
from io import BytesIO
from .models import Cliente
from reportlab.pdfgen import canvas
from orden_trabajo.models import Ordenes_de_trabajo,TareaOrden
from matafuegos.models import Matafuegos

#ACCIONES
from matafuegos_fenix import settings

from parametros.models import Parametros


@admin.action(description='Estado inactivo')
def make_inactivo(modeladmin, request, queryset):
    queryset.update(estado='i')

@admin.action(description='Estado activo')
def make_activo(modeladmin, request, queryset):
    queryset.update(estado='a')

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

def generarInformeCliente(pdf,request,queryset):
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
            matafuegos = Matafuegos.objects.filter(cliente = d.codigo)
            cabeceraTablaMatafuegos(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-22
            for m in matafuegos:
                xlist = [45,132 , 217, 329, 381, 468,560]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(48, y-16, str(m.numero))
                pdf.drawString(135, y-16,str(m.numero_dps))
                if m.direccion != "NULL":
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
            today = date.today()
            td = timedelta(500)
            ordenes= Ordenes_de_trabajo.objects.filter(cliente= d.codigo, fecha_inicio__range=(today-td, today))
            cabeceraTablaOrdenes(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-22
            for o in ordenes:
                xlist = [45, 124, 183, 250, 320, 387, 450, 560]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(48, y-16, str(o.id))
                pdf.drawString(126, y-16, str(o.matafuegos))
                pdf.drawString(185, y-16, str(o.fecha_inicio))
                if o.fecha_cierre:
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
                    if len(nombre)>20:
                        nombre= nombre[0:20]
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
def generarInformeClienteSinOrdenes(pdf,request,queryset):
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
            matafuegos = Matafuegos.objects.filter(cliente = d.codigo)
            cabeceraTablaMatafuegos(pdf,y)
            pdf.setFont("Helvetica", 10)
            y = y-22
            for m in matafuegos:
                xlist = [45,132 , 217, 329, 381, 468,560]
                ylist = [y, y-18]
                pdf.grid(xlist, ylist)
                pdf.drawString(48, y-16, str(m.numero))
                pdf.drawString(135, y-16,str(m.numero_dps))
                if m.direccion != "NULL":
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
        pdf.showPage()
        pdf.save()
@admin.action(description="Enviar informe al cliente")
def send_email(self, request, queryset):
    try:
        pdf = canvas.Canvas("InformeCliente.pdf")
        set = queryset.all()
        if set.count()>1:
            return messages.error(request,'Debe seleccionar solo un cliente')
        else:
            for d in set:
                if d.email:
                     mail_to = d.email
                     nombre= str(d.nombre)
                else:
                     return messages.error(request,'El cliente seleccionado no tiene un email especificado')
        generarInformeClienteSinOrdenes(pdf, request,queryset)
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        info = Parametros.objects.filter(id= 1)
        for i in info:
            email = i.email
            contraseña= i.password
        if not (email and contraseña):
            return messages.error(request,'No hay un email especificado')
        mailServer.login(email,contraseña )
        mensaje = MIMEMultipart()
        with open('InformeCliente.pdf', "rb") as f:
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str('informeCliente.pdf'))
        mensaje.attach(MIMEText('Hola '+ nombre + ', te compartimos el informe con la información de tus matafuegos y las ordenes de trabajo. \n ', 'plain'))
        mensaje.attach(MIMEText('Muchas gracias! ', 'plain'))
        mensaje.attach(attach)
        #IMAGEN
        img_data= open('seguridad_fenix.png', 'rb').read()
        body = MIMEText('<p><img src="cid:seguridad_fenix" /></p>', _subtype='html')
        mensaje.attach(body)
        img = MIMEImage(img_data, 'png')
        img.add_header('Content-Id', '<seguridad_fenix>')  # angle brackets are important
        img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
        mensaje.attach(img)
        mensaje['From'] = email #settings.EMAIL_HOST_USER
        mensaje['To']= mail_to
        mensaje['Subject'] = "Informe Seguridad Fenix"
        mailServer.sendmail(email, mail_to, mensaje.as_string())
        messages.success(request, "Email enviado correctamente")
    except Exception as e:
        print("Error en el envio del email")

#Emite el informe con la informacion de un cliente, los matafuegos que tiene asociado y las tareas.
@admin.action(description="Informe del cliente")
def emitirInformeCliente(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        generarInformeCliente(pdf,request,queryset)
        buffer.seek(0)
        messages.success(request, "Informe emitido")
        return FileResponse(buffer, as_attachment=True, filename='Informe cliente.pdf')


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

    search_fields= ('codigo', 'nombre', 'cuit_cuil','contacto',)
    list_filter= ('estado', 'tipo',)
    actions = [make_inactivo, make_activo, emitirInformeCliente, send_email]
    inlines = [OrdenTrabajoTabularInline, MatafuegoTabularInline]

admin.site.register(Cliente, CLienteAdmin)
