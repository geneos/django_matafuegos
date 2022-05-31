from django.db import models

# Create your models here.
class Parametros(models.Model):
    veh_inicio = models.IntegerField('VEH inicio', default=0)
    veh_fin = models.IntegerField('VEH fin', default=0)
    veh_prefijo = models.CharField('VEH prefijo', max_length=5, default="")
    veh_actual = models.IntegerField('VEH actual', default=0)
    dom_inicio = models.IntegerField('DOM inicio', default=0)
    dom_fin = models.IntegerField('DOM fin', default=0)
    dom_prefijo = models.CharField('DOM prefijo', max_length=5, default="")
    dom_actual = models.IntegerField('DOM actual', default=0)
    email = models.EmailField('Email', blank=True, max_length=264, null=True)
    password = models.CharField('Contraseña',blank=True, max_length=20, null=True)

    class Meta:
        verbose_name_plural = "Parametros"
