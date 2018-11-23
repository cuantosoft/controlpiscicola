from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Finca(models.Model):
    razon_social = models.CharField(max_length=100, unique=True)
    # usuarios = models.ManyToManyField(User)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.razon_social

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Finca, self).save(*args, **kwargs)


class Estanque(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    nivel_agua_mts = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    mts_2 = models.PositiveSmallIntegerField(default=0)
    detalle = models.TextField(blank=True, null=True)
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    estanque = models.ForeignKey(Estanque, on_delete=models.SET_NULL, blank=True, null=True)
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, blank=True, null=True)
    especie = models.CharField(max_length=50, default='tilapia')
    cantidad = models.PositiveIntegerField(default=0)
    tamaño_cm = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    peso_gr = models.PositiveSmallIntegerField(default=0)
    detalle = models.TextField(blank=True, null=True)
    fecha_siembra = models.DateTimeField(auto_now=False, auto_now_add=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


