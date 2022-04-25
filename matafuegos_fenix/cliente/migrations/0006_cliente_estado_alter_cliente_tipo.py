# Generated by Django 4.0.4 on 2022-04-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0005_cliente_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.CharField(choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a', max_length=80, verbose_name='Estado*'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.CharField(choices=[('p', 'Persona'), ('e', 'Empresa')], default='p', max_length=80, verbose_name='Tipo*'),
        ),
    ]
