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

    codigo = models.IntegerField("Codigo", primary_key=True, default=1)
    cuit_cuil = models.CharField('CUIT/CUIL', max_length=11, null=True)
    nombre = models.CharField('Nombre/ Razón Social', max_length=80)
    contacto= models.CharField('Nombre contacto', max_length=80, null= True, blank=True)
    direccion = models.CharField('Dirección', max_length=80, null=True)
    telefono = models.CharField('Telefono', max_length=80, null=True)
    email = models.EmailField('Email', blank=True, max_length=264, null=True)
    web = models.CharField('Web', blank=True, max_length=200, null=True)
    tipo = models.CharField('Tipo', max_length=80, choices=tipos, default= 'p')
    estado = models.CharField('Estado', max_length=80, choices=estados, default= 'a')

    def get_absolute_url(self):
        return reverse('cliente-detalle', args=[str(self.id)])

    def __str__(self):
        return str(self.nombre+" - "+str(self.codigo))

    def save(self, *args, **kwargs):
        self.codigo = int(str(Cliente.objects.raw('SELECT codigo FROM public.cliente_cliente')[-1]).split()[-1])+1
        super(Cliente, self).save(*args, **kwargs)

