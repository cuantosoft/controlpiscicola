from django import forms
from .models import *
from cuser.middleware import CuserMiddleware


class ConcentradoForm(forms.ModelForm):
    class Meta:
        model = Concentrado
        fields = ['nombre', 'proteina', 'kilos', 'precio', 'detalle']

    def clean_nombre(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        coincidencias = Concentrado.objects.filter(finca=user.profile.trabaja_en, nombre=self.nombre).count()
        nombre = self.cleaned_data.get('nombre')
        if coincidencias == 0:
            return nombre
        else:
            raise forms.ValidationError('ya existe un elemento con ese nombre')


class CompraBultosForm(forms.ModelForm):
    user = CuserMiddleware.get_user()
    print(user)
    if user:
        finca = user.profile.trabaja_en
        concentrado = forms.ModelChoiceField(queryset=Concentrado.objects.filter(finca=finca))

    class Meta:
        model = CompradeBultos
        fields = ['concentrado', 'numero_bultos', 'precio_unidad']

