from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Finca(models.Model):
    razon_social = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.razon_social

    def save(self, *args, **kwargs):
        self.slug = slugify(self.razon_social)
        super(Finca, self).save(*args, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------
class Estanque(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    nivel_agua_mts = models.DecimalField(max_digits=5, decimal_places=2,
                                         validators=[MinValueValidator(0)])
    mts_2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    detalle = models.TextField(blank=True, null=True)
    # --------------------------------------------------------------------------------------
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE, blank=True)
    responsable = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    # class Meta:
    #     unique_together = (
    #        ('finca', 'nombre'),
    #     )


# ----------------------------------------------------------------------------------------------------------------------
class Cultivo(models.Model):
    CHOICES = (('siembra', 'siembra'), ('levante', 'levante'), ('engorde', 'engorde'))
    nombre = models.CharField(max_length=100)
    estanque = models.ForeignKey(Estanque, on_delete=models.SET_NULL, null=True)
    especie = models.CharField(max_length=50, default='tilapia')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    tamaño_pez_cm = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    peso_pez_gr = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    densidad_inicial = models.PositiveSmallIntegerField(blank=True, null=True)
    etapa = models.CharField(max_length=7, choices=CHOICES, default='siembra')
    detalle = models.TextField(blank=True, null=True)
    # ----
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100)
    cosechado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_cosecha = models.DateTimeField(blank=True, null=True)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('cultivo_detalle', kwargs={'cultivo_id': self.id})  # f"/products/{self.id}/"

    def total_peces(self):
        total_muertes = 0
        for mortalidad in self.mortalidad_set.all():
            total_muertes += mortalidad.peces_muertos
        return self.cantidad - total_muertes

    def alimento_promedio(self):
        """alimento promedio diario"""
        alimento_total = 0
        alimentacion = self.alimentacion_set.all()
        numero_elementos = alimentacion.count()
        if numero_elementos == 0:
            return 0
        else:
            for alimentacion in alimentacion:
                alimento_total += alimentacion.total()
            promedio = alimento_total / numero_elementos
            return promedio


# @receiver(pre_save, sender=Cultivo)
# def calculos_muestreo(sender, instance, *args, **kwargs):
