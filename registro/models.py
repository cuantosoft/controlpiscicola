from django.db import models

# Create your models here.
class Estanque(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Cultivo(models.Model):
    nombre = models.CharField(max_length=50)
    estanque = models.ForeignKey(Estanque, on_delete=models.SET_NULL, blank=True, null=True,)
    detalle = models.TextField(blank=True, null=True)
    fecha_siembra = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.nombre