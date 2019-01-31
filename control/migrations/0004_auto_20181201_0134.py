# Generated by Django 2.1.2 on 2018-12-01 06:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_auto_20181201_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestreo',
            name='peso_promedio_gr',
            field=models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='muestreo',
            name='talla_promedio_cm',
            field=models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
