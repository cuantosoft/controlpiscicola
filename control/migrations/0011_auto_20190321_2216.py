# Generated by Django 2.1.5 on 2019-03-22 03:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_auto_20190321_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestreo',
            name='a_d',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='ajuste dieta kg'),
        ),
        migrations.AlterField(
            model_name='muestreo',
            name='b',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='biomasa'),
        ),
        migrations.AlterField(
            model_name='muestreo',
            name='f_c_a',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='factor conversion alimenticia'),
        ),
        migrations.AlterField(
            model_name='muestreo',
            name='g_d_p',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='ganancia diaria peso'),
        ),
    ]
