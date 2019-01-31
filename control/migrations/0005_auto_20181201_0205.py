# Generated by Django 2.1.2 on 2018-12-01 07:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_auto_20181201_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='muestreo',
            name='biomasa',
        ),
        migrations.AddField(
            model_name='muestreo',
            name='peso_estimado',
            field=models.DecimalField(decimal_places=1, default=500, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='muestreo',
            name='factor_de_conversion',
            field=models.DecimalField(decimal_places=1, default=1.5, max_digits=6),
        ),
    ]