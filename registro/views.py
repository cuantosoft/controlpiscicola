from django.shortcuts import render
from .models import *
# Create your views here.


def estanque_list(request):
    lista = Estanque.objects.all()
    context = {
        'titulo': 'Mis estanques',
        'estanques': lista
    }
    return render(request, 'registro/estanque_list.html', context)


def cultivo_list(request):
    lista = Cultivo.objects.all()
    context = {
        'titulo': 'Mis cultivos',
        'cultivos': lista
    }
    return render(request, 'registro/cultivo_list.html', context)