from django import forms
from .models import Estanque, Cultivo
from cuser.middleware import CuserMiddleware


# ----estanque forms----------------------------------------------------------------------------------------------------
class EstanqueCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EstanqueCreateForm, self).__init__(*args, **kwargs)
        self.fields['fecha_registro'].widget.attrs['readonly'] = True

    class Meta:
        model = Estanque
        fields = ['nombre', 'tipo', 'nivel_agua_mts', 'mts_2', 'detalle', 'fecha_registro']
        labels = {
            'nivel_agua_mts': 'Nivel agua (m)',
            'mts_2': 'Area (m2)',
        }
        # widgets = {
        #     'nombre': forms.TextInput(attrs={'class': 'input-field'}),
        # }

    def clean_nombre(self):
        user = CuserMiddleware.get_user()
        nombre = self.cleaned_data.get('nombre')
        if Estanque.objects.filter(finca=user.profile.trabaja_en, nombre__iexact=nombre).exists():
            raise forms.ValidationError('ya existe un estanque con ese nombre')
        return nombre


class EstanqueEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.form_estanque_id = kwargs.pop("estanque_id")
        super(EstanqueEditForm, self).__init__(*args, **kwargs)
        self.fields['fecha_registro'].widget.attrs['readonly'] = True

    class Meta:
        model = Estanque
        fields = ['nombre', 'tipo', 'nivel_agua_mts', 'mts_2', 'detalle', 'fecha_registro', 'finca']
        labels = {
            'nivel_agua_mts': 'Nivel agua (m)',
            'mts_2': 'Area (m2)',
        }
        widgets = {
            'finca': forms.HiddenInput()
        }

    def clean(self):
        pk = self.form_estanque_id
        nombre = self.cleaned_data.get('nombre')
        finca = self.cleaned_data.get('finca')
        queryset = Estanque.objects.filter(finca=finca, nombre__iexact=nombre).exclude(id=pk)
        print(pk, nombre, finca, queryset)
        if queryset.exists():
            print('disque existe')
            msg = "ya existe un estanque con ese nombre"
            self.add_error('nombre', msg)


# ----cultivo forms-----------------------------------------------------------------------------------------------------
class CultivoCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CultivoCreateForm, self).__init__(*args, **kwargs)
        user = CuserMiddleware.get_user()
        # self.fields['estanque'].queryset = Estanque.objects.filter(finca=user.profile.trabaja_en)
        self.fields['estanque'] = forms.ModelChoiceField(
            queryset=Estanque.objects.filter(finca=user.profile.trabaja_en))
        self.fields['fecha_registro'].widget.attrs['readonly'] = True
        # self.fields['nombre'].widget.attrs['class'] = 'input-field'

    class Meta:
        model = Cultivo
        fields = ['nombre', 'estanque', 'especie', 'cantidad', 'tamaño_pez_cm', 'peso_pez_gr', 'detalle',
                  'fecha_registro']
        # widgets = {
        #     'finca': forms.HiddenInput()
        # }
        # widgets = {
        #     'fecha_registro': forms.DateTimeField()
        # }

    def clean_nombre(self, *args, **kwargs):
        print(kwargs)
        user = CuserMiddleware.get_user()
        nombre = self.cleaned_data.get('nombre')
        if Cultivo.objects.filter(finca=user.profile.trabaja_en, nombre__iexact=nombre).exists():
            raise forms.ValidationError('ya existe un cultivo con ese nombre')
        return nombre


class CultivoEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.form_cultivo_id = kwargs.pop("cultivo_id")
        super(CultivoEditForm, self).__init__(*args, **kwargs)
        user = CuserMiddleware.get_user()
        self.fields['estanque'] = forms.ModelChoiceField(
            queryset=Estanque.objects.filter(finca=user.profile.trabaja_en))
        self.fields['fecha_registro'].widget.attrs['readonly'] = True

    class Meta:
        model = Cultivo
        fields = ['nombre', 'estanque', 'especie', 'cantidad', 'tamaño_pez_cm', 'peso_pez_gr', 'detalle',
                  'fecha_registro', 'finca']
        widgets = {
            'finca': forms.HiddenInput()
        }

    def clean(self):
        pk = self.form_cultivo_id
        nombre = self.cleaned_data.get('nombre')
        finca = self.cleaned_data.get('finca')
        queryset = Cultivo.objects.filter(finca=finca, nombre__iexact=nombre).exclude(id=pk)

        print(pk, nombre, finca, queryset)
        if queryset.exists():
            print('disque existe')
            msg = "ya existe un cultivo con ese nombre"
            self.add_error('nombre', msg)
