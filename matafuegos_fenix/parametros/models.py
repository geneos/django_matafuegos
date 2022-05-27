from django.db import models

# Create your models here.
class Parametros(models.Model):
    veh_inicio = models.IntegerField('VEH inicio')
    veh_fin = models.IntegerField('VEH fin')
    veh_prefijo = models.CharField('VEH prefijo', max_length=5)
    veh_actual = models.IntegerField('VEH actual')
    dom_inicio = models.IntegerField('DOM inicio')
    dom_fin = models.IntegerField('DOM fin')
    dom_prefijo = models.CharField('DOM prefijo', max_length=5)
    dom_actual = models.IntegerField('DOM actual')
    email = models.EmailField('Email', blank=True, max_length=264)
    password = models.CharField('Contraseña',blank = True, max_length=20)

    class Meta:
        verbose_name_plural = "Parametros"
