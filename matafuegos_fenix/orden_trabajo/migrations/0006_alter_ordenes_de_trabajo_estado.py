# Generated by Django 4.0.4 on 2022-07-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden_trabajo', '0005_alter_ordenes_de_trabajo_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes_de_trabajo',
            name='estado',
            field=models.CharField(choices=[('p', 'Pendiente'), ('ep', 'En proceso'), ('f', 'Finalizada'), ('c', 'Cancelada')], default='ep', max_length=80, verbose_name='Estado'),
        ),
    ]
