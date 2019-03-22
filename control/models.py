from django.db import models
from registro.models import Estanque, Cultivo, Finca
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from inventario.models import Concentrado
# user = settings.AUTH_USER_MODEL


class Mortalidad(models.Model):
    peces_muertos = models.PositiveSmallIntegerField(default=0)
    # ----
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    responsable = models.CharField(settings.AUTH_USER_MODEL, max_length=100)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Mortalidad cultivo: {}'.format(self.cultivo.nombre)


class Muestreo(models.Model):
    talla_promedio_cm = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    peso_promedio_gr = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    valor_ajuste_tabla = models.DecimalField(default=2.0, max_digits=6, decimal_places=1,
                                             validators=[MinValueValidator(0.0)])
    observaciones = models.TextField(blank=True, null=True)
    # ---- congelar resultados
    b = models.DecimalField('biomasa', max_digits=7, decimal_places=2, validators=[MinValueValidator(0.0)],
                            blank=True, null=True)
    a_d = models.DecimalField('ajuste dieta kg', max_digits=7, decimal_places=2, validators=[MinValueValidator(0.0)],
                              blank=True, null=True)
    g_d_p = models.DecimalField('ganancia diaria peso', max_digits=7, decimal_places=2,
                                validators=[MinValueValidator(0.0)], blank=True, null=True)
    f_c_a = models.DecimalField('factor conversion alimenticia', max_digits=7, decimal_places=2,
                               validators=[MinValueValidator(0.0)], blank=True, null=True)
    # ----
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'muestreo cultivo: {}'.format(self.cultivo.nombre)

    # ---- calculos muestreo
    def peso_anterior(self):
        ultimo_muestreo = Muestreo.objects.filter(cultivo=self.cultivo, fecha_registro__lt=self.fecha_registro).last()
        if ultimo_muestreo is None:
            peso_anterior = self.cultivo.peso_pez_gr
        else:
            peso_anterior = ultimo_muestreo.peso_promedio_gr
        print('peso anterior', peso_anterior)
        return peso_anterior

    def biomasa(self):
        total_peces = self.cultivo.total_peces()
        peso_anterior = self.peso_anterior()
        biomasa = (total_peces * peso_anterior) / 1000  # Kg
        print('total peces', total_peces)
        print('biomasa', biomasa)
        return biomasa

    def ajuste_dieta(self):
        ajuste_dieta = self.biomasa() * (self.valor_ajuste_tabla / 100)
        print('ajuste_dieta', ajuste_dieta)
        return ajuste_dieta

    def fecha_ultimo_muestreo(self):
        print('self fecha', self.fecha_registro)
        ultimo_muestreo = Muestreo.objects.filter(cultivo=self.cultivo, fecha_registro__lt=self.fecha_registro).last()
        print('ultimo_muestreo filter', ultimo_muestreo)
        if ultimo_muestreo is None:
            fecha_ultimo_muestreo = self.cultivo.fecha_registro
        else:
            fecha_ultimo_muestreo = ultimo_muestreo.fecha_registro
        print('fecha ultimo muestreo', fecha_ultimo_muestreo)
        return fecha_ultimo_muestreo

    def delta_fecha(self):
        delta_fecha = self.fecha_registro - self.fecha_ultimo_muestreo()
        delta_fecha = delta_fecha.days
        print('delta_fecha', delta_fecha)
        return delta_fecha

    def delta_peso(self):
        delta_peso = self.peso_promedio_gr - self.peso_anterior()
        print('delta peso', delta_peso)
        return delta_peso

    def ganancia_diaria_peso(self):
        if self.delta_fecha() == 0:
            ganancia_diaria_peso = -1
        else:
            ganancia_diaria_peso = self.delta_peso() / self.delta_fecha()
        print('ganacia diraria peso', ganancia_diaria_peso)
        return ganancia_diaria_peso

    def factor_conversion_alimenticia(self):
        alimento_utilizado = Alimentacion.alimento_suministrado(self.cultivo, self.fecha_ultimo_muestreo())
        factor_conversion_alimenticia = alimento_utilizado / float(self.delta_peso())
        print('factor de conversion alimenticia:', factor_conversion_alimenticia)
        return factor_conversion_alimenticia


@receiver(pre_save, sender=Muestreo)
def calculos_muestreo(sender, instance, *args, **kwargs):
    instance.b = instance.biomasa()
    instance.a_d = instance.ajuste_dieta()
    instance.g_d_p = instance.ganancia_diaria_peso()
    instance.f_c_a = instance.factor_conversion_alimenticia()


"""
Tabla de alimentación (Cultivo semi-intensivo intensivo).
 Edad     Peso-Promedio Crecimiento-Diario Alimento-Diario Conversión-Alimenticia.
(Semanas)(gramos)      (gr/día).         (% de peso).
0           1     15 0.83
1           3     0.27 10 0.85
2           5     0.27 8 0.85
3           7     0.34 5.8 0.86
4           10    0.36 5.7 0.9
5           13    0.46 5.5 0.9
6           17    0.58 5.1 0.9
7           22    0.71 5.1 0.91
8           29    0.93 5.0 0.95
9           37    1.14 4.5 0.98
10          46    1.29 4.3 0.98
11          56    1.51 4.2 1.0
12          69    1.79 4.1 1.03
13          83    2.07 4.0 1.03
14          100   2.43 4.0 1.1
15          120   2.85 3.5 1.15
16          140   2.86 3.4 1.15
17          162   3.14 3.2 1.25
18          184   3.14 2.9 1.25
19          207   3.29 2.8 1.26
20          231   3.43 2.6 1.28
21          256   3.57 2.4 1.28
22          282   3.71 2.3 1.28
23          309   3.85 2.2 1.3
24          337   4.0 2.1 1.37
25          355   4.0 1.9 1.37
26          393   4.0 1.8 1.37
27          422   4.14 1.7 1.37
28          451   4.14 1.6 1.37
29          480   4.14 1.5 1.34
30          509   4.14 1.4 1.34
31          538   4.14 1.4 1.35
32          567   4.14 1.4 1.45
33          596   4.14 1.3 1.47
34          629   4.14 1.3 1.49
35          654   4.14 1.2 1.49
36          683   4.14 1.1 1.65"""


# ----Alimentación------------------------------------------------------------------------------------------------------
class Alimentacion(models.Model):
    dia = models.DateField(auto_now_add=True)
    # ----
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)

    def __str__(self):
        return "Alimentacion día: {}".format(self.dia)

    def total(self):
        total = 0
        for racion in self.racion_set.all():
            total += racion.cantidad_gr

        return total

    @staticmethod
    def alimento_suministrado(cultivo, fecha):
        # alimentación desde una fecha en adelante
        total_alimento_reciente = 0.0
        alimentacion = Alimentacion.objects.filter(cultivo_id=cultivo)
        if alimentacion.count() > 0:
            alimentacion_reciente = alimentacion.filter(dia__gte=fecha)
            if alimentacion_reciente.count() > 0:
                for alimento in alimentacion_reciente:
                    total_alimento_reciente = total_alimento_reciente + alimento.total()
        print('total_alimento_reciente', total_alimento_reciente)
        return total_alimento_reciente


class Racion(models.Model):
    cantidad_gr = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    tipo_concentrado = models.ForeignKey(Concentrado, on_delete=models.CASCADE)
    # ----
    alimentacion = models.ForeignKey(Alimentacion, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'ranción de{}'.format(self.alimentacion)


"""
Rango de peso (gramos) Nivel óptimo de proteína (%).
Larva a 0.5 40 - 45 %
0.5 . a 10 . 40 - 35 %
10 . a 30 30 - 35 %
30 a 250 30 - 35 %
250 a talla de mercado. 25 - 30 %

"""


# ----Calidad del agua--------------------------------------------------------------------------------------------------
class Calidad_agua(models.Model):
    oxigeno = models.DecimalField('Oxígeno mg/l', max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    temperatura = models.DecimalField('Temperatura °C', max_digits=4, decimal_places=1, validators=[MinValueValidator(-10), MaxValueValidator(100)])
    dureza = models.PositiveSmallIntegerField('Dureza mg/l', validators=[MinValueValidator(0)])  # mg/l
    ph = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(14)])
    amonio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    nitritos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    nitratos = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    co2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    # ----
    estanque = models.ForeignKey(Estanque, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'calidad agua estanque: {} id: {}'.format(self.estanque.nombre, self.pk)


class Rangos_calidad_agua(models.Model):
    max_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    min_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
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
    min_co2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    max_co2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    # ----
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)

    def __str__(self):
        return 'rangos finca: {}'.format(self.finca.razon_social)


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



