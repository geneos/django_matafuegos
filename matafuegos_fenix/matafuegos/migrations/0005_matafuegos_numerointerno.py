# Generated by Django 4.0.4 on 2022-06-15 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matafuegos', '0004_alter_matafuegos_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='matafuegos',
            name='numeroInterno',
            field=models.IntegerField(blank=True, null=True, verbose_name='Numero interno'),
        ),
    ]
