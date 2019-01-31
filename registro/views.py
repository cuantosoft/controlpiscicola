from django.shortcuts import render, redirect
from .models import *
from .forms import  EstanqueCreateForm, CultivoCreateForm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# principio
def la_piscicola(request):
    try:
        la_piscicola = request.user.profile.trabaja_en
        if  'la_piscicola' not in request.session:
            request.session['la_piscicola']=la_piscicola.id
    except:
        la_piscicola = None
        # raise Http404("Este usuario no tiene un finca asignada")
    context = {
        'la_piscicola': la_piscicola
    }
    return render(request,'registro/la_piscicola.html', context)


# estanque views
def estanque_list(request):
    finca = None
    lista = None
    if request.user.is_authenticated:
        # print(request.session['la_piscicola'])
        finca = request.user.profile.trabaja_en
        #                               finca__id=request.session['la_piscicola']
        lista = Estanque.objects.filter(finca=finca).order_by('-fecha_registro')
        mensaje = 'consulta exitosa'
        if finca is None:
            mensaje = 'no perteneces a ninguna finca consulta con el administrador'
    else:
        mensaje='error: no ha iniciado sesión'
    context = {
        'la_piscicola': finca,
        'titulo': 'Mis estanques',
        'estanques': lista,
        'mensaje': mensaje
    }
    return render(request, 'registro/estanque_list.html', context)

def estanque_crear(request):
    print(request)
    if request.method == 'POST':
        form = EstanqueCreateForm(request.POST or None)
        if form.is_valid():
            estanque = form.save(commit=False)
            estanque.finca = request.user.profile.trabaja_en
            estanque.responsable = request.user
            estanque.save()
            return redirect('estanque_list')
    else:
        form = EstanqueCreateForm()
    context={
        'form': form,
        'titulo': ' Nuevo estanque'
    }
    return render(request, 'registro/estanque_crear.html', context)


def estanque_detalle(request, estanque_id):
    estanque =get_object_or_404(Estanque, pk=estanque_id)
    return render(request,'registro/estanque_detalle.html', {'estanque': estanque})


def estanque_editar(request, estanque_id):
    objeto = get_object_or_404(Estanque, pk=estanque_id)
    form = EstanqueCreateForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect('estanque_detalle', estanque_id)
    context={
        'form': form,
        'titulo': 'Editar estanque'
    }
    return render(request, 'registro/estanque_crear.html', context)


# cultivo views
def cultivo_list(request):
    finca=None
    lista=None
    if request.user.is_authenticated:
        finca = request.user.profile.trabaja_en
        lista = Cultivo.objects.filter(finca=finca, cosechado=False).order_by('-fecha_registro')
        mensaje = 'consulta exitosa'
        if finca is None:
            mensaje = 'tu cuenta no esta asociada a ninguna finca consulta con el administrador'
    else:
        mensaje='error: no ha iniciado sesión'

    context = {
        'la_piscicola': finca,
        'titulo': 'Mis cultivos',
        'cultivos': lista,
        'mensaje': mensaje
    }
    return render(request, 'registro/cultivo_list.html', context)


@login_required
def cultivo_crear(request):
    form = CultivoCreateForm()
    if request.method == 'POST':
        form = CultivoCreateForm(request.POST)
        if form.is_valid():
            cultivo = form.save(commit=False)
            cultivo.finca = request.user.profile.trabaja_en
            cultivo.responsable = request.user
            cultivo.save()
            return redirect('cultivo_list')
    context = {
        'form': form,
        'titulo': 'Nuevo cultivo'
    }
    return render(request, 'registro/cultivo_crear.html', context)


def cultivo_detalle(request, cultivo_id):
    try:
        cultivo = Cultivo.objects.get(pk=cultivo_id)
    except Cultivo.DoesNotExist:
        raise Http404("no existe ese cultivo")
    return render(request,'registro/cultivo_detalle.html', {'cultivo': cultivo})

def cultivo_editar(request, cultivo_id):
    objeto = get_object_or_404(Cultivo, pk=cultivo_id)
    form = CultivoCreateForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect('cultivo_detalle', cultivo_id)
    context={
        'form': form,
        'titulo': 'Editar cultivo'
    }
    return render(request, 'registro/cultivo_crear.html', context)

def cosecha_list(request):
    finca = None
    lista = None
    if request.user.is_authenticated:
        finca = request.user.profile.trabaja_en
        lista = Cultivo.objects.filter(finca=finca, cosechado=True).order_by('-fecha_update')
        mensaje = 'consulta exitosa'
        if finca is None:
            mensaje = 'tu cuenta no esta asociada a ninguna finca consulta con el administrador'
    else:
        mensaje = 'error: no ha iniciado sesión'

    context = {
        'la_piscicola': finca,
        'titulo': 'Mis cosechas',
        'cosechas': lista,
        'mensaje': mensaje
    }
    return render(request, 'registro/cultivo_list.html', context)
