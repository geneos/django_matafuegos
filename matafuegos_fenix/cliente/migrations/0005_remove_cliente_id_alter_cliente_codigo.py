# Generated by Django 4.0.4 on 2022-06-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_alter_cliente_email_alter_cliente_web'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='id',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='codigo',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Codigo'),
        ),
    ]
