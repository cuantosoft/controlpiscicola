from django.shortcuts import render, redirect
from .models import *
from .forms import EstanqueCreateForm, EstanqueEditForm, CultivoCreateForm, CultivoEditForm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView,CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def la_piscicola(request):  # página inicial logeado
    la_piscicola_obj = request.user.profile.trabaja_en
    print(request.user.profile.trabaja_en)
    if la_piscicola_obj is not None:
        if 'la_piscicola' not in request.session:
            request.session['la_piscicola'] = la_piscicola_obj.id
    # raise Http404("Este usuario no tiene un finca asignada")
    else:
        messages.error(request, 'el usuario no esta asignado a ninguna finca')
    context = {
        'la_piscicola': la_piscicola_obj
    }
    return render(request, 'registro/la_piscicola.html', context)

# ----estanque views----------------------------------------------------------------------------------------------------
@login_required
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


@login_required
def estanque_crear(request):
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


@login_required
def estanque_detalle(request, estanque_id):
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    return render(request,'registro/estanque_detalle.html', {'estanque': estanque})


@login_required
def estanque_editar(request, estanque_id):
    objeto = get_object_or_404(Estanque, pk=estanque_id)
    form = EstanqueEditForm(request.POST or None, instance=objeto, estanque_id=estanque_id)
    if form.is_valid():
        form.save()
        return redirect('estanque_detalle', estanque_id)
    context = {
        'form': form,
        'titulo': 'Editar estanque'
    }
    return render(request, 'registro/estanque_crear.html', context)


# ----cultio views------------------------------------------------------------------------------------------------------
@login_required
def cultivo_list(request):
    finca = None
    lista = None
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
            peso = form.cleaned_data['peso_pez_gr']
            if 40 < peso < 120:
                cultivo.etapa = "levante"
                cultivo.save()
            if peso >= 120:
                cultivo.etapa = "engorde"
                cultivo.save()
            else:
                cultivo.save()
            return redirect('cultivo_list')
    context = {
        'form': form,
        'titulo': 'Nuevo cultivo'
    }
    return render(request, 'registro/cultivo_crear.html', context)


@login_required
def cultivo_detalle(request, cultivo_id):
    try:
        cultivo = Cultivo.objects.get(pk=cultivo_id)
    except Cultivo.DoesNotExist:
        raise Http404("no existe ese cultivo")
    return render(request, 'registro/cultivo_detalle.html', {'cultivo': cultivo})


@login_required
def cultivo_editar(request, cultivo_id):
    objeto = get_object_or_404(Cultivo, pk=cultivo_id)
    form = CultivoEditForm(request.POST or None, instance=objeto, cultivo_id=cultivo_id)
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            print('es valido')
            cultivo = form.save(commit=False)
            peso = cultivo.peso_pez_gr
            if 40 < peso < 120:
                cultivo.etapa = "levante"
                cultivo.save()
            if peso >= 120:
                cultivo.etapa = "engorde"
                cultivo.save()
            else:
                cultivo.save()
            return redirect('cultivo_detalle', cultivo_id)
    context = {
        'form': form,
        'titulo': 'Editar cultivo'
    }
    return render(request, 'registro/cultivo_crear.html', context)


@login_required
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
    return render(request, 'registro/cosecha_list.html', context)


def cultivo_cosechar(request, cultivo_id):
    cultivo = Cultivo.objects.get(pk=cultivo_id)
    if request.method == 'POST':
        cultivo.cosechado = True
        cultivo.fecha_cosecha = datetime.now()
        cultivo.save()
        return redirect('cosecha_list')
    context = {
        'cultivo': cultivo,
    }
    return render(request, 'registro/cultivo_cosechar.html', context)



