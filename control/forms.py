from django.forms import ModelForm
from .models import *


class MortalidadForm(ModelForm):
    class Meta:
        model = Mortalidad
        fields = ['peces_muertos']


class Muestreo(ModelForm):
    class Meta:
        model = Muestreo
        fields = ['talla_promedio_cm', 'peso_promedio_gr']


class AlimentacionForm(ModelForm):
    class Meta:
        model = Racion
        fields = ['cantidad_gr', 'tipo_concentrado']


class CalidadAguaForm(ModelForm):
    class Meta:
        model = Calidad_agua
        exclude = ['estanque','responsable', 'fecha_registro', 'fecha_update']


class Rangos_calidad_aguaForm(ModelForm):
    class Meta:
        model = Rangos_calidad_agua
        fields = '__all__'
