# Generated by Django 4.0.4 on 2022-04-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matafuegos', '0005_alter_matafuegos_numero_localizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='matafuegos',
            name='categoria',
            field=models.CharField(choices=[('v', 'Vehicular'), ('d', 'Domiciliario')], default=1, max_length=80, verbose_name='Categoria'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='matafuegos',
            name='numero_localizacion',
            field=models.IntegerField(blank=True, null=True, verbose_name='Numero de localizacion'),
        ),
    ]
