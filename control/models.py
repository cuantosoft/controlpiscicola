from django.db import models
from registro.models import Estanque, Cultivo, Finca
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


# Create your models here.
class Mortalidad(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    peces_muertos = models.PositiveSmallIntegerField(default=0)
    responsable = models.CharField(settings.AUTH_USER_MODEL, max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)


class Muestreo(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

    talla_promedio_cm = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    peso_promedio_gr = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    factor_de_conversion = models.DecimalField(default=1.5, max_digits=6, decimal_places=1)
    peso_estimado = models.DecimalField(default=500, max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])

    ganancia_diaria_peso = models.DecimalField(max_digits=6, decimal_places=2)
    biomasa = models.DecimalField(max_digits=6, decimal_places=2)
    ajuste_dieta = models.PositiveSmallIntegerField()
    observaciones = models.TextField()
    # ----------------------------------------------------
    # finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)

    def gdp(self):  # ganancia diaria de peso
        fecha_inicial = self.cultivo.fecha_registro
        fecha_actual = self.fecha_registro
        delta_peso = self.peso_promedio_gr - self.cultivo.peso_pez_gr
        delta_fecha = self.fecha_registro - self.cultivo.fecha_registro
        delta_dias = delta_fecha.days
        if delta_dias == 0:
            gdp = 0
        else:
            gdp = delta_peso / delta_dias
        return gdp

    def alimento_estimado(self):
        return self.factor_de_conversion * self.peso_estimado

    def biomasa(self):
        return ((self.cultivo.peso_pez_gr + self.ganancia_diaria_peso) * self.cultivo.total_peces()) / 1000  # Kg


"""
Tabla de alimentación (Cultivo semi-intensivo intensivo).
 Edad     Peso-Promedio Crecimiento-Diario Alimento-Diario Conversión-Alimenticia.
(Semanas)(gramos)      (gr/día).         (% de peso).
0           1 15 0.83
1           3 0.27 10 0.85
2           5 0.27 8 0.85
3           7 0.34 5.8 0.86
4           10 0.36 5.7 0.9
5           13 0.46 5.5 0.9
6           17 0.58 5.1 0.9
7           22 0.71 5.1 0.91
8           29 0.93 5.0 0.95
9           37 1.14 4.5 0.98
10          46 1.29 4.3 0.98
11          56 1.51 4.2 1.0
12          69 1.79 4.1 1.03
13          83 2.07 4.0 1.03
14          100 2.43 4.0 1.1
15          120 2.85 3.5 1.15
16          140 2.86 3.4 1.15
17          162 3.14 3.2 1.25
18          184 3.14 2.9 1.25
19          207 3.29 2.8 1.26
20          231 3.43 2.6 1.28
21          256 3.57 2.4 1.28
22          282 3.71 2.3 1.28
23          309 3.85 2.2 1.3
24          337 4.0 2.1 1.37
25          355 4.0 1.9 1.37
26          393 4.0 1.8 1.37
27          422 4.14 1.7 1.37
28          451 4.14 1.6 1.37
29          480 4.14 1.5 1.34
30          509 4.14 1.4 1.34
31          538 4.14 1.4 1.35
32          567 4.14 1.4 1.45
33          596 4.14 1.3 1.47
34          629 4.14 1.3 1.49
35          654 4.14 1.2 1.49
36          683 4.14 1.1 1.65"""


# --------------------------------------------------------------------------------------
class Alimentacion(models.Model):
    dia = models.DateField(auto_now_add=True)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

    def __str__(self):
        return "Alimentacion: {}".format(self.dia)

    def total(self):
        total = 0
        for racion in self.racion_set.all():
            total += racion.cantidad_gr

        return "{}".format(total)


class Racion(models.Model):
    alimentacion = models.ForeignKey(Alimentacion, on_delete=models.CASCADE)

    cantidad_gr = models.PositiveSmallIntegerField()
    tipo_concentrado = models.CharField(max_length=100)
    # ----------------------------------------------------
    # finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.alimentacion)


"""
Rango de peso (gramos) Nivel óptimo de proteína (%).
Larva a 0.5 40 - 45 %
0.5 . a 10 . 40 - 35 %
10 . a 30 30 - 35 %
30 a 250 30 - 35 %
250 a talla de mercado. 25 - 30 %


"""


# --------------------------------------------------------------------------------------
class Calidad_agua(models.Model):
    estanque = models.ForeignKey(Estanque, on_delete=models.CASCADE)
    # ---------------------------------------------------------------------------------
    oxigeno = models.DecimalField('Oxígeno', max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    temperatura = models.PositiveSmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(100)])
    dureza = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    ph = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(14)])
    amonio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    nitritos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    nitratos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    co2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    # ----------------------------------------------------
    # finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)


class Rangos_calidad_agua(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    # ---------------------------------------------------------------------------------
    max_oxigeno = models.DecimalField('Oxígeno', max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    min_oxigeno = models.DecimalField('Oxígeno', max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    max_temperatura = models.PositiveSmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(100)])
    min_temperatura = models.PositiveSmallIntegerField(validators=[MinValueValidator(-10), MaxValueValidator(100)])
    max_ph = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(14)])
    min_ph = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(14)])
    max_amonio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    min_amonio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    max_nitritos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    min_nitritos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    max_nitratos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    min_nitratos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])


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
    precio = models.DecimalField(max_digits=8, decimal_places=2)


class CompradeBultos(models.Model):
    concentrado = models.ForeignKey(Concentrado, on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField()
