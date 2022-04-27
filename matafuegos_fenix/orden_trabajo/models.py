from datetime import date

from django.db import models

from cliente.models import Cliente

from matafuegos.models import Matafuegos


class Tarea(models.Model):
    nombre = models.CharField('Nombre', max_length=120)
    precio = models.FloatField("Precio", default=0)

    def __str__(self):
        return self.nombre

estados= [
    ('p','Pendiente'),
    ('ep','En proceso'),
    ('f','Finalizada'),
    ('c','cancelada'),
]


class Ordenes_de_trabajo(models.Model):
    numero = models.IntegerField("Numero", default=0)
    fecha = models.DateField("Fecha de realización",default= date.today)
    fecha_entrega= models.DateField("Fecha de entrega estimada", default= date.today)
    fecha_cierre= models.DateField("Fecha de cierre", blank= True, null=True)
    notas = models.CharField('notas', max_length=80, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.CharField('Estado', max_length=80, choices=estados, default= 'p')
    monto_total = models.FloatField('monto', default=0)
    matafuegos = models.ForeignKey(Matafuegos, on_delete=models.CASCADE)

    def calcular_monto(self):
        monto=0
        for p in Tarea_Orden.objects.filter(orden=self.numero).values_list('tarea'):
            monto+= Tarea.objects.filter(id=p[0]).values_list('precio')[0][0]
        return monto


    def save(self, *args, **kwargs ):
        self.monto_total= self.calcular_monto()
        super(Ordenes_de_trabajo,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.numero)

    class Meta:
      verbose_name_plural = "Ordenes de trabajo"

class Tarea_Orden(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    orden = models.ForeignKey(Ordenes_de_trabajo, on_delete=models.CASCADE)

    def save(self, *args, **kwargs ):
        super(Tarea_Orden,self).save(*args, **kwargs)
        self.orden.save()

    class Meta:
        verbose_name_plural = "Tarea - Orden de trabajo"
