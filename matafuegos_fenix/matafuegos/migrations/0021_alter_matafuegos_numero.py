# Generated by Django 4.0.4 on 2022-07-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matafuegos', '0020_alter_matafuegos_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matafuegos',
            name='numero',
            field=models.IntegerField(verbose_name='Numero'),
        ),
    ]
