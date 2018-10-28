from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Finca(models.Model):
    razon_social = models.CharField(max_length=100, unique=True)
    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return self.razon_social


class Estanque(models.Model):
    nombre = models.CharField(max_length=100)
    detalle = models.TextField(blank=True, null=True)
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    estanque = models.ForeignKey(Estanque, on_delete=models.SET_NULL, blank=True, null=True)
    finca = models.ForeignKey(Finca, on_delete=models.SET_NULL, blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    fecha_siembra = models.DateTimeField(auto_now=False, auto_now_add=True)
    responsable = models.CharField(max_length=100, default='----')

    def __str__(self):
        return self.nombre


