from django.shortcuts import render
from registro.models import Finca


def inicio(request):

    mensaje = 'Si ya tienes una cuenta dale a la opción ingresar del menú'
    la_piscicola = None

    if request.user.is_authenticated:
        try:
            finca = request.user.profile.trabaja_en
            print(finca)
            mensaje='bienvenido a la finca: {}'.format(finca)
            la_piscicola = finca
        except Finca.DoesNotExist:
            mensaje = 'No has configurado tu finca, comunícate con el administrador'

    context = {
        'mensaje': mensaje,
        'la_piscicola': la_piscicola
    }
    return render(request, 'base.html', context)



