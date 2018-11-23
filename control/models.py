from django.db import models
from registro.models import Estanque, Cultivo, Finca
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Muestreo(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

    talla_promedio_cm = models.PositiveSmallIntegerField()
    peso_promedio_gr = models.PositiveSmallIntegerField()
    # mts_2

    peces_muertos = models.PositiveSmallIntegerField()
    ganancia_diaria_peso = models.DecimalField(max_digits=6,decimal_places=2)
    factor_de_conversion = models.DecimalField(max_digits=6,decimal_places=2)
    biomasa = models.DecimalField(max_digits=6,decimal_places=2)
    ajuste_dieta = models.PositiveSmallIntegerField()
    observaciones = models.TextField()
    #----------------------------------------------------
    # finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)


# --------------------------------------------------------------------------------------
class Alimentacion(models.Model):
    dia = models.DateField(auto_now_add=True)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

class Racion(models.Model):
    alimentacion = models.ForeignKey(Alimentacion, on_delete=models.CASCADE)

    cantidad_gr = models.PositiveSmallIntegerField()
    tipo_concentrado = models.CharField(max_length=100)
    # ----------------------------------------------------
    # finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)


# --------------------------------------------------------------------------------------
class Calidad_agua(models.Model):
    estanque = models.ForeignKey(Estanque, on_delete=models.CASCADE)

    oxigeno = models.DecimalField('Oxígeno',max_digits=5,decimal_places=2,validators=[MinValueValidator(0.00)])
    temperatura = models.PositiveSmallIntegerField('Temperatura', validators=[MinValueValidator(-10), MaxValueValidator(100)])
    dureza = models.PositiveSmallIntegerField('Dureza',validators=[MinValueValidator(0)])
    ph = models.PositiveSmallIntegerField('pH',validators=[MinValueValidator(0), MaxValueValidator(14)])
    amonio = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.00)])
    nitritos = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.00)])
    nitratos = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.00)])
    co2 = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.00)])
    # ----------------------------------------------------
    # finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)

"""
    **oxigeno mg/L**
0.0 - 0.3 Los peces pequeños sobreviven en cortos períodos.
0.3 - 2.0 Letal a exposiciones prolongadas.
3.0 - 4.0 L os peces sobreviven pero crecen lentamente.
    > 4.5 Rango deseable para el crecimiento del pez.
    **temperatura °C**
28°-32°
    **dureza ppm**
50-350 ppm de CaCO
100ppma 200ppm alcalinidad
    **ph**
6.5 - 9.0
    **amonio ppm**
0.01 - 0.1
0.6 - 2.0 tilapia
    **nitritos ppm**
    < 0.1
    **nitratos ppm**
    < 40
"""

class Concentrado(models.Model):
    nombre = models.CharField(max_length=100)
    proteina = models.PositiveSmallIntegerField()
    kilos = models.PositiveSmallIntegerField()
    precio = models.DecimalField(max_digits=8,decimal_places=2)

class CompraBultos(models.Model):
    concentrado = models.ForeignKey(Concentrado, on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField()
