from django.db import models

# Create your models here.
class Parametros(models.Model):
    veh_inicio = models.IntegerField('VEH Inicio')
    veh_fin = models.IntegerField('VEH Fin')
    veh_prefijo = models.CharField('VEH Prefijo', max_length=5)
    veh_actual = models.IntegerField('VEH Actual')
    dom_inicio = models.IntegerField('DOM Inicio')
    dom_fin = models.IntegerField('DOM Fin')
    dom_prefijo = models.CharField('DOM Prefijo', max_length=5)
    dom_actual = models.IntegerField('DOM Actual')
    class Meta:
        verbose_name_plural = "Parametros"
