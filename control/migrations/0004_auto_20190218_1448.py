# Generated by Django 2.1.5 on 2019-02-18 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_remove_muestreo_biomasa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='muestreo',
            name='Factor_conversion_alimenticia',
        ),
        migrations.RemoveField(
            model_name='muestreo',
            name='ajuste_dieta',
        ),
        migrations.RemoveField(
            model_name='muestreo',
            name='ganancia_diaria_peso',
        ),
    ]
