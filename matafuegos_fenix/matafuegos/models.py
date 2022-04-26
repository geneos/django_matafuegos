import datetime

from django.db import models

# Create your models here.
from cliente.models import Cliente



class CategoriaMatafuegos(models.Model):
    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Categoria Matafuegos"

class TipoMatafuegos(models.Model):
    tipo = models.CharField('Tipo', max_length=100)
    categoria = models.ForeignKey(CategoriaMatafuegos, on_delete=models.CASCADE)
    vencimiento_carga = models.IntegerField('Vencimiento de carga')
    vencimiento_ph = models.IntegerField('Vencimiento de PH')
    volumen = models.FloatField('Volumen')
    peso = models.FloatField('Peso')

    def __str__(self):
        return self.tipo
    class Meta:
        verbose_name_plural = "Tipo Matafuegos"

class MarcaMatafuegos(models.Model):
    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Marca Matafuegos"

class Matafuegos(models.Model):
    numero = models.IntegerField('Numero')
    numero_bv = models.IntegerField('Numero de BV')
    numero_dps = models.IntegerField('Numero de DPS')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    patente = models.CharField('Patente', max_length=20, blank=True)
    direccion = models.CharField('Direccion', max_length=100)
    localización = models.CharField('Localizacion', max_length=100, blank=True)
    numero_localizacion = models.IntegerField('Numero de localizacion', null=True, blank=True)
    marca = models.ForeignKey(MarcaMatafuegos, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMatafuegos, on_delete=models.CASCADE)
    cat = [('v', 'Vehicular'),('d', 'Domiciliario'),]
    categoria = models.CharField('Categoria', max_length=100, choices=cat)
    centro_costo = models.CharField('Centro de costo', max_length=100)
    fecha_fabricación = models.DateField()
    fecha_carga = models.DateField(default=datetime.date.today)
    fecha_proxima_carga = models.DateField(null=True, blank=True)
    fecha_ph = models.DateField(default=datetime.date.today)
    fecha_proxima_ph = models.DateField(null=True, blank=True)

    def calcularFecha(self, fecha, dias):
        return fecha + datetime.timedelta(days=dias)

    def save(self, *args, **kwargs):
        self.fecha_proxima_carga = self.calcularFecha(self.fecha_carga, self.tipo.vencimiento_carga)
        self.fecha_proxima_ph = self.calcularFecha(self.fecha_ph, self.tipo.vencimiento_ph)
        super(Matafuegos, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Matafuegos"
