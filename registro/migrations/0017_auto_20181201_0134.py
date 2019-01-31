# Generated by Django 2.1.2 on 2018-12-01 06:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0016_cultivo_fecha_cosecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cultivo',
            name='peso_pez_gr',
            field=models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='cultivo',
            name='tamaño_pez_cm',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='estanque',
            name='nivel_agua_mts',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
