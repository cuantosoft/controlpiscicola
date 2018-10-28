from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
# Create your views here.
def pagina_error(request):
    return render(request, 'error.html', {})

def la_piscicola(request):
    try:
        la_piscicola = Finca.objects.get(usuarios=request.user)
        context={
            'la_piscicola': la_piscicola
        }
    except Finca.DoesNotExist:
        raise Http404("Este usuario no tiene un finca asignada")
    print (request.user)
    return render(request,'registro/la_piscicola.html', context)


def estanque_list(request, piscicola_id):
    finca=Finca.objects.get(id=piscicola_id)
    lista = Estanque.objects.filter(finca=finca)
    context = {
        'la_piscicola': finca,
        'titulo': 'Mis estanques',
        'estanques': lista
    }
    return render(request, 'registro/estanque_list.html', context)


def cultivo_list(request, piscicola_id):
    finca = Finca.objects.get(id=piscicola_id)
    lista = Cultivo.objects.filter(finca=finca)
    context = {
        'la_piscicola': finca,
        'titulo': 'Mis cultivos',
        'cultivos': lista
    }
    return render(request, 'registro/cultivo_list.html', context)