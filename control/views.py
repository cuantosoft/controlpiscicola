from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, reverse
from .models import *
from .forms import *
import datetime


def muestreo_listar(request,cultivo_id):
    cultivo = get_object_or_404(Cultivo, pk=cultivo_id)
    muestreo_list = Alimentacion.objects.filter(id=cultivo_id)
    context={
        'cultivo': cultivo,
        'muestreo_list': muestreo_list
    }
    return render(request, 'control/muestreo_list.html', context)


def muestreo_registrar(request, cultivo_id):
    pass


def muestreo_editar(request, cultivo_id, muestreo_id):
    pass


def mortalidad_registrar(request, cultivo_id):
    form = MortalidadForm()
    cultivo = get_object_or_404(Cultivo, pk=cultivo_id)
    if request.method == 'POST':
        form = MortalidadForm(request.POST)
        if form.is_valid():
            mortalidad = form.save(commit=False)
            mortalidad.cultivo = cultivo
            # caliagua.responsable = request.user
            mortalidad.save()
            return redirect('cultivo_list')
    return render(request, 'control/mortalidad_registrar.html', {'form': form, 'cultivo': cultivo})


# ----------------------------------------------------------------------------------------------------------------------
def alimentacion_listar(request,cultivo_id):
    cultivo = Cultivo.objects.get(id=cultivo_id)
    alimentacion_list = Alimentacion.objects.filter(cultivo=cultivo_id)
    return render(request,'control/alimentacion_list.html', {'alimentacion_list': alimentacion_list, 'cultivo': cultivo})


def alimentacion_registrar(request, cultivo_id):
    # ración
    hoy = datetime.date.today()
    print(hoy)
    cultivo=Cultivo.objects.get(id=cultivo_id)
    form = AlimentacionForm()
    try:
        alimentacion = Alimentacion.objects.get(dia=hoy, cultivo=cultivo)
    except Alimentacion.DoesNotExist:
        alimentacion = Alimentacion.objects.create(dia=hoy, cultivo=cultivo)
    print(alimentacion.dia==hoy)
    if request.method == 'POST':
        print('es post')
        form=AlimentacionForm(request.POST)
        if form.is_valid:
            print('es valido')
            f = form.save(commit=False)
            cantidad_gr=form.cleaned_data['cantidad_gr']
            tipo_concentrado=form.cleaned_data['tipo_concentrado']
            f.cantidad_gr=cantidad_gr
            f.tipo_concentrado=tipo_concentrado
            f.responsable = request.user
            f.alimentacion = alimentacion
            f.save()
            return redirect('cultivo_list')
    return render(request, 'control/racion.html', {'form': form, 'alimentacion': alimentacion, 'cultivo': cultivo})


def alimentacion_editar(request, cultivo_id, alimentacion_id):
    pass


# ----------------------------------------------------------------------------------------------------------------------
def calidad_agua_listar(request, estanque_id):
    estanque=get_object_or_404(Estanque.objects.order_by('-fecha_registro'), pk=estanque_id)
    calidad_agua_list=Calidad_agua.objects.filter(estanque_id=estanque_id).order_by('-fecha_registro')
    context={
        'estanque': estanque,
        'caliagua_list': calidad_agua_list
    }
    return render(request, 'control/calidad_agua_list.html', context)


def calidad_agua_registrar(request, estanque_id):
    form = CalidadAguaForm()
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    if request.method=='POST':
        form = CalidadAguaForm(request.POST)
        if form.is_valid():
            caliagua = form.save(commit=False)
            caliagua.estanque = estanque
            caliagua.responsable = request.user
            caliagua.save()
            # return redirect('estanque_list')
            return redirect('estanque_detalle', estanque_id)
    return render(request, 'control/calidad_agua_registrar.html', {'form': form, 'estanque': estanque})


def calidad_agua_editar(request, estanque_id, calidad_agua_id):
    caliagua = get_object_or_404(Calidad_agua, pk=calidad_agua_id)
    form = CalidadAguaForm(request.POST or None, instance=caliagua)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('control:calidad_agua_listar', estanque_id)
    return render(request,'control/calidad_agua_registrar.html', {"form": form})


def calidad_agua_detalle(request, estanque_id, calidad_agua_id):
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    caliagua = get_object_or_404(Calidad_agua, pk=calidad_agua_id)
    return render(request, 'control/calidad_agua_detalle.html', {"caliagua": caliagua, "estanque":estanque})

def graficas_agua(request, estanque_id):
    estanque = get_object_or_404(Estanque, id=estanque_id)
    queryset = Calidad_agua.objects.filter(estanque=estanque)
    fechas=[]
    oxigeno=[]
    for object in queryset:
        oxigeno.append(float(object.oxigeno))
        fechas.append(object.fecha_registro.strftime('%d-%m-%Y'))

    context = {
        "estanque": estanque,
        "object_list": queryset,
        "oxigeno": oxigeno,
        "fechas": fechas
    }
    return render(request, 'control/graficas_agua.html', context)
