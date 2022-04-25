from django.db import models


class Tarea(models.Model):

    nombre = models.CharField('Nombre', max_length=120)

    def __str__(self):
        return self.nombre

class Ordenes_de_trabajo(models.Model):
    nombre = models.CharField('Nombre', max_length=120)
    #cliente = models.ForeignKey(Cliente, db_column='codigo')

    def __str__(self):
        return self.nombre
