# Generated by Django 4.0.4 on 2022-07-11 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0008_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(max_length=80, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=80, null=True, verbose_name='Telefono'),
        ),
    ]
