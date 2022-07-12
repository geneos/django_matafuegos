from datetime import date
from django.contrib import admin
from django.db import models
from django.urls import reverse
from cliente.models import Cliente
from matafuegos.models import Matafuegos

class Tarea(models.Model):
    nombre = models.CharField('Nombre', max_length=120)
    precio = models.FloatField("Precio", default=0)

    def get_absolute_url(self):
        return reverse('tarea-detalle', args=[str(self.id)])

    def __str__(self):
        return str(self.nombre+" - $"+str(self.precio))


estados = [
    ('p', 'Pendiente'),
    ('ep', 'En proceso'),
    ('f', 'Finalizada'),
    ('c', 'Cancelada'),
]

class Ordenes_de_trabajo(models.Model):

    fecha_creacion = models.DateField("Fecha de creacioin de orden", default=date.today)
    fecha_inicio = models.DateField("Fecha de inicio", blank=True, null=True,default=date.today)
    fecha_entrega= models.DateField("Entrega estimada", default=date.today)
    fecha_cierre= models.DateField("Fecha de cierre", blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    matafuegos = models.ForeignKey(Matafuegos, on_delete=models.CASCADE)
    estado = models.CharField('Estado', max_length=80, choices=estados, default= 'ep')
    monto_total = models.FloatField('Monto', default=0)
    notas = models.CharField('Notas', max_length=80, blank=True)
    impresa= models.BooleanField('Impresa', default=False)


    def calcular_monto(self):
        monto=0
        i=0
        for p in TareaOrden.objects.filter(orden=self).values_list('tarea'):
            if TareaOrden.objects.filter(orden=self).values_list('precioAj')[i][0] == 0.0:
                monto+= Tarea.objects.filter(id=p[0]).values_list('precio')[0][0]
            else:
                monto+= TareaOrden.objects.filter(orden=self).values_list('precioAj')[i][0]
            i+=1
        return monto


    @admin.display(boolean=True)
    def estados(self):
        if self.estado in ['f', 'c']:
            return False
        return True

    def save(self, *args, **kwargs ):
        self.monto_total = self.calcular_monto()
        #self.cliente = self.matafuegos.cliente
        super(Ordenes_de_trabajo,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ordenes_de_trabajo-detalle', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

    class Meta:
      verbose_name_plural = "Ordenes de trabajo"

class TareaOrden(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    orden = models.ForeignKey(Ordenes_de_trabajo, on_delete=models.CASCADE)
    precioAj = models.FloatField('precio ajustable', default=0)
    cant_cargada = models.FloatField('Cantidad Cargada', default=0)

    def save(self, *args, **kwargs):
        super(TareaOrden, self).save(*args, **kwargs)
        self.orden.save()

    def get_absolute_url(self):
        return reverse('tarea_orden-detalle', args=[str(self.id)])

    class Meta:
        verbose_name_plural = "Tarea - Orden de trabajo"

    def __str__(self):
        return str(self.id)

