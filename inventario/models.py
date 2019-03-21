from django.db import models
from django.utils import timezone
from registro.models import Finca


class Concentrado(models.Model):
    """Para registrar los tipos de concentrado a utilizar"""
    nombre = models.CharField(max_length=100)
    proteina = models.PositiveSmallIntegerField('Proteina %')
    kilos = models.PositiveSmallIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    total_kg = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    detalle = models.TextField(blank=True, null=True)
    # ----
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nombre)


class CompradeBultos(models.Model):
    """Para registrar las cantidades de concentrado comprado"""
    concentrado = models.ForeignKey(Concentrado, on_delete=models.CASCADE)
    numero_bultos = models.PositiveSmallIntegerField()
    precio_unidad = models.DecimalField(max_digits=8, decimal_places=2)
    # ----
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "bultos {}".format(self.concentrado)
