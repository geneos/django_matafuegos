import unittest
from django.test import TestCase

from cliente.models import Cliente


class ClienteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Cliente.objects.create(codigo= 1, cuit_cuil=4343, telefono=2222, nombre='Big', direccion='San Lorenzo 516',tipo="p", estado='i')
    pass

    def test_codigo_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('codigo').verbose_name
        self.assertEquals(field_label,'Codigo')

    def test_cuit_cuil_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('cuit_cuil').verbose_name
        self.assertEquals(field_label,'CUIT/CUIL')

    def test_nombre_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('nombre').verbose_name
        self.assertEquals(field_label,'Nombre/ Razón Social')

    def test_nombre_max_length(self):
        cliente=Cliente.objects.get(id=1)
        max_length = cliente._meta.get_field('nombre').max_length
        self.assertEquals(max_length,80)

    def test_direccion_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('direccion').verbose_name
        self.assertEquals(field_label,'Dirección')

    def test_direccion_max_length(self):
        cliente = Cliente.objects.get(id=1)
        max_length = cliente._meta.get_field('direccion').max_length
        self.assertEquals(max_length,80)

    def test_telefono_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('telefono').verbose_name
        self.assertEquals(field_label,'Telefono')

    def test_nombre_max_length(self):
        cliente = Cliente.objects.get(id=1)
        max_length = cliente._meta.get_field('telefono').max_length
        self.assertEquals(max_length, 14)

    def test_email_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('email').verbose_name
        self.assertEquals(field_label,'Email')

    def test_email_max_length(self):
        cliente=Cliente.objects.get(id=1)
        max_length = cliente._meta.get_field('email').max_length
        self.assertEquals(max_length,264)

    def test_web_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('web').verbose_name
        self.assertEquals(field_label,'Web')

    def test_web_max_length(self):
        cliente = Cliente.objects.get(id=1)
        max_length = cliente._meta.get_field('web').max_length
        self.assertEquals(max_length,200)

    def test_tipo_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('tipo').verbose_name
        self.assertEquals(field_label,'Tipo')

    def test_estado_label(self):
        cliente = Cliente.objects.get(id=1)
        field_label = cliente._meta.get_field('estado').verbose_name
        self.assertEquals(field_label,'Estado')

    def test_get_absolute_url(self):
        cliente=Cliente.objects.get(id=1)


