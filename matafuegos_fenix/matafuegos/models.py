from datetime import date
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponse

# Create your models here.
from cliente.models import Cliente

class CategoriaMatafuegos(models.Model):
    nombre = models.CharField('Nombre', max_length=20)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Categoria Matafuegos"

class TipoMatafuegos(models.Model):
    tipo = models.CharField('Tipo', max_length=20)
    categoria = models.ForeignKey(CategoriaMatafuegos, on_delete=models.CASCADE, null=True, blank=True)
    vencimiento_carga = models.IntegerField('Vencimiento de carga', help_text="Cantidad de dias", null=True, blank=True)
    vencimiento_ph = models.IntegerField('Vencimiento de PH', help_text="Cantidad de dias", null=True, blank=True)
    volumen = models.FloatField('Volumen', null=True, blank=True)
    peso = models.FloatField('Peso', null=True, blank=True)

    def __str__(self):
        return self.tipo
    class Meta:
        verbose_name_plural = "Tipo Matafuegos"

class MarcaMatafuegos(models.Model):
    nombre = models.CharField('Nombre', max_length=15)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Marca Matafuegos"

class Matafuegos(models.Model):
    numero = models.IntegerField('Numero')
    numeroInterno= models.IntegerField('Numero interno',blank=True, null= True)
    numero_dps = models.IntegerField('Numero de DPS', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    patente = models.CharField('Patente', max_length=19, blank=True, null= True)
    direccion = models.CharField('Direccion', max_length=30, null=True, blank=True)
    localizacion = models.CharField('Localizacion', max_length=60, blank=True, null= True)
    numero_localizacion = models.IntegerField('Numero de localizacion', null=True, blank=True)
    marca = models.ForeignKey(MarcaMatafuegos, on_delete=models.CASCADE, null=True)
    tipo = models.ForeignKey(TipoMatafuegos, on_delete=models.CASCADE)
    cat = [('v', 'Vehicular'),('d', 'Domiciliario'),('ma', 'Maquinaria Agricola')]
    categoria = models.CharField('Categoria', max_length=20, choices=cat)
    fecha_fabricacion = models.DateField('Fecha de fabricacion', null=True)
    fecha_carga = models.DateField('Fecha de carga',default=datetime.date.today, null= True)
    fecha_proxima_carga = models.DateField('Fecha de proxima carga',null=True, blank=True)
    fecha_ph = models.DateField('Fecha de PH',default=datetime.date.today, null=True)
    fecha_proxima_ph = models.DateField('Fecha de proxima PH',null=True, blank=True)
    vencido = models.BooleanField('Vencido', default= False)

    def calcularFecha(self, fecha, dias):
        return fecha + datetime.timedelta(days=dias)

    def save(self, *args, **kwargs):
        if self.categoria == 'ma':
            self.patente='Maquina agricola'
        self.fecha_proxima_carga = self.calcularFecha(self.fecha_carga, self.tipo.vencimiento_carga)
        self.fecha_proxima_ph = self.calcularFecha(self.fecha_ph, self.tipo.vencimiento_ph)
        super(Matafuegos, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Matafuegos"

    def __str__(self):
        return str(str(self.numero) + "-" + str(self.tipo))

    #@background(schedule=60)
    #def matafuegos_vencidos(self):
    #    matafuegos = Matafuegos.objects.all()
    #    for m in matafuegos:
    #        if (date.today() - m.fecha_fabricacion).days/365 > 20:
    #            m.vencido = True
    #            m.save()


