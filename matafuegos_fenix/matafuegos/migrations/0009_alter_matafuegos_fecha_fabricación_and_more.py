# Generated by Django 4.0.4 on 2022-04-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matafuegos', '0008_alter_matafuegos_fecha_fabricación_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matafuegos',
            name='fecha_fabricación',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='matafuegos',
            name='fecha_proxima_ph',
            field=models.DateField(editable=False),
        ),
    ]
