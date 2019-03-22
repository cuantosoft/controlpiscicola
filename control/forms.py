from django import forms
from .models import *
from cuser.middleware import CuserMiddleware


class MortalidadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MortalidadForm, self).__init__(*args, **kwargs)
        self.fields['fecha_registro'].widget.attrs['readonly'] = True

    class Meta:
        model = Mortalidad
        fields = ['peces_muertos', 'fecha_registro']


class MuestreoForm(forms.ModelForm):
    class Meta:
        model = Muestreo
        fields = ['peso_promedio_gr', 'talla_promedio_cm', 'valor_ajuste_tabla', 'observaciones', 'fecha_registro']


class AlimentacionForm(forms.ModelForm):  # en realidad es racion
    def __init__(self, *args, **kwargs):
        super(AlimentacionForm, self).__init__(*args, **kwargs)
        user = CuserMiddleware.get_user()
        self.fields['tipo_concentrado'] = forms.ModelChoiceField(
            queryset=Concentrado.objects.filter(finca=user.profile.trabaja_en))

    class Meta:
        model = Racion
        fields = ['cantidad_gr', 'tipo_concentrado', 'fecha_registro']


class CalidadAguaForm(forms.ModelForm):
    class Meta:
        model = Calidad_agua
        exclude = ['estanque','responsable', 'fecha_registro', 'fecha_update']


class CalidadAguaRangosForm(forms.ModelForm):  # las clases hazlas con camelCase
    class Meta:
        model = Rangos_calidad_agua
        fields = '__all__'
        exclude = ['finca']
