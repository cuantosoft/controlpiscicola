# Generated by Django 2.1.1 on 2019-01-29 18:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0017_auto_20181201_0134'),
        ('control', '0005_auto_20181201_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rangos_calidad_agua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_oxigeno', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Oxígeno')),
                ('min_oxigeno', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Oxígeno')),
                ('max_temperatura', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(100)])),
                ('min_temperatura', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(100)])),
                ('max_ph', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(14)])),
                ('min_ph', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(14)])),
                ('max_amonio', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('min_amonio', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('max_nitritos', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('min_nitritos', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('max_nitratos', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('min_nitratos', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('finca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registro.Finca')),
            ],
        ),
    ]