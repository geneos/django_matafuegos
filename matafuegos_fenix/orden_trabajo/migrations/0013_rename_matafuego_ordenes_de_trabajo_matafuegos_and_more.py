# Generated by Django 4.0.4 on 2022-04-27 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden_trabajo', '0012_alter_ordenes_de_trabajo_fecha_cierre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordenes_de_trabajo',
            old_name='matafuego',
            new_name='matafuegos',
        ),
        migrations.AlterField(
            model_name='ordenes_de_trabajo',
            name='monto_total',
            field=models.FloatField(default=0, verbose_name='monto'),
        ),
    ]
