from django.test import TestCase
from parametros.models import Parametros

class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        parametros = Parametros.objects.create(veh_inicio=1,
                                                veh_fin=2,
                                                veh_prefijo='3',
                                                veh_actual=4,
                                                dom_inicio=5,
                                                dom_fin=6,
                                                dom_prefijo='7',
                                                dom_actual=8)

        pass

    # ETIQUETAS ------------------------------------------------------------------------------------------------

    def test_veh_inicio_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('veh_inicio').verbose_name
        self.assertEquals(field_label,'VEH inicio')

    def test_veh_fin_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('veh_fin').verbose_name
        self.assertEquals(field_label,'VEH fin')

    def test_veh_prefijo_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('veh_prefijo').verbose_name
        self.assertEquals(field_label,'VEH prefijo')

    def test_veh_actual_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('veh_actual').verbose_name
        self.assertEquals(field_label,'VEH actual')

    def test_dom_inicio_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('dom_inicio').verbose_name
        self.assertEquals(field_label,'DOM inicio')

    def test_dom_fin_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('dom_fin').verbose_name
        self.assertEquals(field_label,'DOM fin')

    def test_dom_prefijo_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('dom_prefijo').verbose_name
        self.assertEquals(field_label,'DOM prefijo')

    def test_dom_actual_label(self):
        parametros = Parametros.objects.get(id=1)
        field_label = parametros._meta.get_field('dom_actual').verbose_name
        self.assertEquals(field_label,'DOM actual')

    # LONGITUD -------------------------------------------------------------------------------------------------

    def test_veh_prefijo_length(self):
        parametros = Parametros.objects.get(id=1)
        max_length = parametros._meta.get_field('veh_prefijo').max_length
        self.assertEquals(max_length,5)

    def test_dom_prefijo_length(self):
        parametros = Parametros.objects.get(id=1)
        max_length = parametros._meta.get_field('dom_prefijo').max_length
        self.assertEquals(max_length,5)

"""
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
"""
