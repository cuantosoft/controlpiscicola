from django.shortcuts import render
from registro.models import Finca
# Create your views here.

def inicio(request):

    if request.user.is_authenticated:
        finca=Finca.objects.get(usuarios=request.user)
        context={
            'la_piscicola': finca
        }
    context={
        'mensaje': 'Hola'
    }
    return render(request, 'base.html', context)