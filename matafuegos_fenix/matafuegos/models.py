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
    numero_dps = models.IntegerField('Numero de DPS')
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    patente = models.CharField('Patente', max_length=10, blank=True, null= True)
    direccion = models.CharField('Direccion', max_length=20, null=True, blank=True)
    localizacion = models.CharField('Localizacion', max_length=20, blank=True, null= True)
    numero_localizacion = models.IntegerField('Numero de localizacion', null=True, blank=True)
    marca = models.ForeignKey(MarcaMatafuegos, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMatafuegos, on_delete=models.CASCADE)
    cat = [('v', 'Vehicular'),('d', 'Domiciliario'),]
    categoria = models.CharField('Categoria', max_length=12, choices=cat)
    fecha_fabricacion = models.DateField('Fecha de fabricacion')
    fecha_carga = models.DateField('Fecha de carga',default=datetime.date.today)
    fecha_proxima_carga = models.DateField('Fecha de proxima carga',null=True, blank=True)
    fecha_ph = models.DateField('Fecha de PH',default=datetime.date.today)
    fecha_proxima_ph = models.DateField('Fecha de proxima PH',null=True, blank=True)


    def calcularFecha(self, fecha, dias):
        return fecha + datetime.timedelta(days=dias)

    def save(self, *args, **kwargs):
        self.fecha_proxima_carga = self.calcularFecha(self.fecha_carga, self.tipo.vencimiento_carga)
        self.fecha_proxima_ph = self.calcularFecha(self.fecha_ph, self.tipo.vencimiento_ph)
        super(Matafuegos, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Matafuegos"

    def __str__(self):
        return str(self.numero)


