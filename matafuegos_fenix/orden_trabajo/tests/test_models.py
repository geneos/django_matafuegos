from datetime import date

from django.test import TestCase

from orden_trabajo.models import Tarea, Ordenes_de_trabajo, Tarea_Orden

from cliente.models import Cliente

from matafuegos.models import MarcaMatafuegos, CategoriaMatafuegos, TipoMatafuegos, Matafuegos


class TareaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Tarea.objects.create(nombre='limpiar', precio=100)

    def test_nombre_label(self):
        tarea = Tarea.objects.get(id=1)
        field_label = tarea._meta.get_field('nombre').verbose_name
        self.assertEquals(field_label,'Nombre')

    def test_nombre_max_length(self):
        tarea = Tarea.objects.get(id=1)
        max_length = Tarea._meta.get_field('nombre').max_length
        self.assertEquals(max_length,120)

    def test_precio_label(self):
        tarea = Tarea.objects.get(id=1)
        field_label = tarea._meta.get_field('precio').verbose_name
        self.assertEquals(field_label,'Precio')

    def test_get_absolute_url(self):
        tarea=Tarea.objects.get(id=1)


class OrdenesTrabajoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        marca = MarcaMatafuegos.objects.create(nombre = 'abc')

        categoria = CategoriaMatafuegos.objects.create(nombre = 'categoria 1')

        tipo = TipoMatafuegos.objects.create(tipo = 'tipo 1',
                                             categoria = categoria,
                                             vencimiento_carga = 10,
                                             vencimiento_ph = 20,
                                             volumen = 5.5,
                                             peso = 10)

        cliente = Cliente.objects.create(codigo = 789,
                               cuit_cuil = 987,
                               nombre = 'Victoria Dell Oso',
                               direccion = 'chacabuco 1147',
                               telefono = '2492565089',
                               email = 'maylendelloso@gmail.com',
                               tipo = 'Persona',
                               estado = 'Activo')

        matafuegos = Matafuegos.objects.create(numero = 987,
                                  numero_bv = 9,
                                  numero_dps = 8,
                                  cliente = cliente,
                                  direccion = 'chacabuco 1147',
                                  marca = marca,
                                  tipo = tipo,
                                  categoria = 'Domiciliario',
                                  centro_costo = '005',
                                  fecha_fabricacion = date(2022,4,28),
                                  fecha_carga = date(2022,4,28),
                                  fecha_ph = date(2022,4,28))

        Ordenes_de_trabajo.objects.create(numero=11, fecha= date(2022,4,26), fecha_entrega=date(2022,4,28), fecha_cierre= date(2022,4,28), cliente= cliente, estado= 'p', matafuegos= matafuegos)
    pass

    def test_numero_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('numero').verbose_name
        self.assertEquals(field_label,'Numero')

    def test_fecha_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('fecha').verbose_name
        self.assertEquals(field_label,'Fecha de realización')

    def test_fecha_entrega_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('fecha_entrega').verbose_name
        self.assertEquals(field_label,'Fecha de entrega estimada')

    def test_fecha_cierre_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('fecha_cierre').verbose_name
        self.assertEquals(field_label,'Fecha de cierre')

    def test_notas_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('notas').verbose_name
        self.assertEquals(field_label,'notas')

    def test_notas_max_length(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        max_length = orden._meta.get_field('notas').max_length
        self.assertEquals(max_length, 80)

    def test_cliente_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('cliente').verbose_name
        self.assertEquals(field_label,'cliente')

    def test_estado_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('estado').verbose_name
        self.assertEquals(field_label,'Estado')

    def test_montototal_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('monto_total').verbose_name
        self.assertEquals(field_label,'Monto')

    def test_matafuegos_label(self):
        orden = Ordenes_de_trabajo.objects.get(id=1)
        field_label = orden._meta.get_field('matafuegos').verbose_name
        self.assertEquals(field_label,'matafuegos')


class Orden_tareaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
      #  tarea= Tarea.objects.create(nombre='limpieza', precio='100')
        marca = MarcaMatafuegos.objects.create(nombre = 'abc')

        categoria = CategoriaMatafuegos.objects.create(nombre = 'categoria 1')

        tipo = TipoMatafuegos.objects.create(tipo = 'tipo 1',
                                             categoria = categoria,
                                             vencimiento_carga = 10,
                                             vencimiento_ph = 20,
                                             volumen = 5.5,
                                             peso = 10)

        cliente = Cliente.objects.create(codigo = 789,
                               cuit_cuil = 987,
                               nombre = 'Victoria Dell Oso',
                               direccion = 'chacabuco 1147',
                               telefono = '2492565089',
                               email = 'maylendelloso@gmail.com',
                               tipo = 'Persona',
                               estado = 'Activo')

        matafuegos = Matafuegos.objects.create(numero = 987,
                                  numero_bv = 9,
                                  numero_dps = 8,
                                  cliente = cliente,
                                  direccion = 'chacabuco 1147',
                                  marca = marca,
                                  tipo = tipo,
                                  categoria = 'Domiciliario',
                                  centro_costo = '005',
                                  fecha_fabricacion = date(2022,4,28),
                                  fecha_carga = date(2022,4,28),
                                  fecha_ph = date(2022,4,28))
        #tarea= Tarea.objects.create(nombre='limpieza', precio='100')
        #orden= Ordenes_de_trabajo.objects.create(numero=11, fecha= date(2022,4,26), fecha_entrega=date(2022,4,28), fecha_cierre= date(2022,4,28), cliente= cliente, estado= 'p', matafuegos= matafuegos)
        #CHEQUEAR ESTO
        Tarea_Orden.objects.create(tarea= Tarea.objects.get(id=1), orden= Ordenes_de_trabajo.objects.get(id=1))
    pass

    def test_tarea_label(self):
        tarea = Tarea_Orden.objects.get(id=1)
        field_label = tarea._meta.get_field('tarea').verbose_name
        self.assertEquals(field_label,'tarea')

    def test_orden_label(self):
        orden = Tarea_Orden.objects.get(id=1)
        field_label = orden._meta.get_field('orden').verbose_name
        self.assertEquals(field_label,'orden')
"""
    def test_montoTotal_label(self):
        orden = Tarea_Orden.objects.get(id=1)
        field_label = orden._meta.get_field('monto_total').verbose_name
        self.assertEquals(orden.save(),200)
        print(orden)
"""
