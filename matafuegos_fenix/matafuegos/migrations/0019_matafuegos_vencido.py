# Generated by Django 4.0.4 on 2022-07-08 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matafuegos', '0018_alter_matafuegos_fecha_fabricacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='matafuegos',
            name='vencido',
            field=models.BooleanField(default=False, verbose_name='Vencido'),
        ),
    ]
