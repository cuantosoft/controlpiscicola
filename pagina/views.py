from django.shortcuts import render
from registro.models import Finca
# Create your views here.

def inicio(request):
    context={}
    if request.user.is_authenticated:
        try:
            finca = request.user.profile.trabaja_en
            print(finca)
            mensaje='bienvenido a la finca: {}'.format(finca)
            la_piscicola = finca
        except Finca.DoesNotExist:
            mensaje = 'No has configurado tu finca, comunícate con el administrador'
            la_piscicola = None
    context = {
        'mensaje': mensaje,
        'la_piscicola': finca
    }
    return render(request, 'base.html', context)