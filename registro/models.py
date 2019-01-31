from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse

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
    tipo = models.CharField(max_length=100, blank=True, null=True)
    nivel_agua_mts = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0)])
    mts_2 = models.PositiveSmallIntegerField('superficie_mts_2',default=0)
    detalle = models.TextField(blank=True, null=True)
    # --------------------------------------------------------------------------------------
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# ----------------------------------------------------------------------------------------------------------------------
class Cultivo(models.Model):
    CHOICES = (('siembra','siembra'),('levante','levante'),('engorde','engorde'))
    nombre = models.CharField(max_length=100)
    estanque = models.ForeignKey(Estanque, on_delete=models.SET_NULL, null=True)
    especie = models.CharField(max_length=50, default='tilapia')
    cantidad = models.PositiveIntegerField(default=0)
    tamaño_pez_cm = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, validators=[MinValueValidator(0)])
    peso_pez_gr = models.DecimalField(max_digits=5,decimal_places=1, validators=[MinValueValidator(0)])
    densidad_inicial = models.PositiveSmallIntegerField(blank=True, null=True)
    etapa = models.CharField(max_length=7, choices=CHOICES, default='siembra')
    detalle = models.TextField(blank=True, null=True)
    # --------------------------------------------------------------------------------------
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    cosechado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_cosecha = models.DateTimeField(blank=True,null=True)
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('cultivo_detalle', kwargs={'cultivo_id': self.id}) # f"/products/{self.id}/"

    def total_peces(self):
        total_muertes=0
        for mortalidad in self.mortalidad_set.all():
            total_muertes+=mortalidad.peces_muertos
        return self.cantidad-total_muertes


