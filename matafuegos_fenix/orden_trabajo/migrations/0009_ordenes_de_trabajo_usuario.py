# Generated by Django 4.0.4 on 2022-07-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden_trabajo', '0008_remove_ordenes_de_trabajo_impresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenes_de_trabajo',
            name='usuario',
            field=models.CharField(default='', max_length=30, verbose_name='Usuario respondable'),
        ),
    ]
