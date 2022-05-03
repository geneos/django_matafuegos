from django.db import models
from django.urls import reverse

estados = [
        ('a', 'Activo'),
        ('i', 'Inactivo'),
    ]

class Cliente(models.Model):
    tipos = [
        ('p', 'Persona'),
        ('e', 'Empresa'),
    ]

    codigo = models.IntegerField("Codigo")
    cuit_cuil = models.CharField('CUIT/CUIL', max_length=11)
    nombre = models.CharField('Nombre/ Razón Social', max_length=80)
    direccion = models.CharField('Dirección', max_length=80)
    telefono = models.CharField('Telefono', max_length=14)
    email = models.EmailField('Email', blank=True, max_length=264)
    web = models.CharField('Web', blank=True, max_length=200)
    tipo = models.CharField('Tipo', max_length=80, choices=tipos, default= 'p')
    estado = models.CharField('Estado', max_length=80, choices=estados, default= 'a')

    def get_absolute_url(self):
        return reverse('cliente-detalle', args=[str(self.id)])

    def __str__(self):
        return str(self.nombre+" - "+str(self.codigo))
