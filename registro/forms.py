from django import forms
from .models import Estanque, Cultivo
from cuser.middleware import CuserMiddleware


class EstanqueCreateForm(forms.ModelForm):
    class Meta:
        model = Estanque
        fields = ['nombre','tipo','nivel_agua_mts','mts_2','detalle','fecha_registro']
        labels = {
            'mts_2': 'Area mts 2',
        }

    def __init__(self, *args, **kwargs):
        super(EstanqueCreateForm, self).__init__(*args, **kwargs)
        self.fields['fecha_registro'].widget.attrs['readonly'] = True


class CultivoCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CultivoCreateForm, self).__init__(*args, **kwargs)
        user = CuserMiddleware.get_user()
        self.fields['estanque'].queryset=Estanque.objects.filter(finca=user.profile.trabaja_en)
        self.fields['fecha_registro'].widget.attrs['readonly'] = True

    class Meta:
        model = Cultivo
        fields = ['nombre','estanque','especie','cantidad','tamaño_pez_cm','peso_pez_gr','detalle','fecha_registro']
        # widgets = {
        #     'fecha_registro': forms.DateTimeField()
        # }
