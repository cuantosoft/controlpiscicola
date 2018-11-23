from django.shortcuts import render, redirect
from .models import *
# from .forms import CultivoSiembraForm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView

# Create your views here.
def pagina_error(request):
    return render(request, 'error.html', {})

def la_piscicola(request):
    try:
        la_piscicola = request.user.profile.trabaja_en
    except:
        la_piscicola = None
        # raise Http404("Este usuario no tiene un finca asignada")
    context = {
        'la_piscicola': la_piscicola
    }
    return render(request,'registro/la_piscicola.html', context)


def estanque_list(request):

    finca = request.user.profile.trabaja_en
    lista = Estanque.objects.filter(finca=finca)
    context = {
        'la_piscicola': finca,
        'titulo': 'Mis estanques',
        'estanques': lista
    }
    return render(request, 'registro/estanque_list.html', context)


def cultivo_list(request):

    finca = request.user.profile.trabaja_en
    lista = Cultivo.objects.filter(finca=finca)
    context = {
        'la_piscicola': finca,
        'titulo': 'Mis cultivos',
        'cultivos': lista
    }
    return render(request, 'registro/cultivo_list.html', context)

def cultivo_siembra(request):
    pass

