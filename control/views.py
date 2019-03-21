from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from datetime import datetime
import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def muestreo_listar(request, cultivo_id):
    cultivo = get_object_or_404(Cultivo, pk=cultivo_id)
    muestreo_list = Muestreo.objects.filter(cultivo=cultivo_id)
    context = {
        'cultivo': cultivo,
        'muestreo_list': muestreo_list
    }
    return render(request, 'control/muestreo_list.html', context)


@login_required
def muestreo_registrar(request, cultivo_id):
    cultivo = get_object_or_404(Cultivo, pk=cultivo_id)
    form = MuestreoForm()
    if request.method == 'POST':
        form = MuestreoForm(request.POST)
        if form.is_valid():
            muestreo = form.save(commit=False)
            muestreo.cultivo = cultivo
            muestreo.responsable = request.user
            # muestreo.b = muestreo.biomasa()
            # muestreo.a_d = muestreo.ajuste_dieta()
            # muestreo.g_d_p = muestreo.ganancia_diaria_peso()
            # muestreo.f_c_a#  = muestreo.factor_conversion_alimenticia()
            muestreo.save()
            # http://documentacion.ideam.gov.co/openbiblio/bvirtual/001819/Winisis/Pagina/ord_cont10.htm
            peso = form.cleaned_data['peso_promedio_gr']
            if 40 < peso < 120:
                cultivo.etapa = "levante"
                cultivo.save()
            if peso >= 120:
                cultivo.etapa = "engorde"
                cultivo.save()
            return redirect('cultivo_detalle', cultivo_id)

    context = {
        'cultivo': cultivo,
        'form': form
    }
    return render(request, 'control/muestreo_registrar.html', context)


@login_required
def muestreo_editar(request, cultivo_id, muestreo_id):
    pass


@login_required
def grafica_muestreo(request, cultivo_id):
    cultivo = get_object_or_404(Cultivo, id=cultivo_id)
    muestreos = Muestreo.objects.filter(cultivo=cultivo)
    fechas = []
    peso = []
    talla = []
    for muestreo in muestreos:
        peso.append(float(muestreo.peso_promedio_gr))
        fechas.append(muestreo.fecha_registro.strftime('%d-%m-%Y'))
        talla.append(float(muestreo.talla_promedio_cm))

    context = {
        "cultivo": cultivo,
        "object_list": muestreos,
        "peso": peso,
        "fechas": fechas,
        "talla": talla,
    }
    return render(request, 'control/grafica_muestreo.html', context)


@login_required
def mortalidad_registrar(request, cultivo_id):
    form = MortalidadForm()
    cultivo = get_object_or_404(Cultivo, pk=cultivo_id)
    if request.method == 'POST':
        form = MortalidadForm(request.POST)
        if form.is_valid():
            mortalidad = form.save(commit=False)
            peces_muertos = form.cleaned_data.get('peces_muertos')
            if peces_muertos == 0:
                messages.info(request, 'no se registró mortalidad.')
                return redirect('cultivo_detalle', cultivo_id)
            mortalidad.cultivo = cultivo
            mortalidad.responsable = request.user
            mortalidad.save()
            return redirect('cultivo_detalle', cultivo_id)
    return render(request, 'control/mortalidad_registrar.html', {'form': form, 'cultivo': cultivo})


# ----alimentación----------------------------------------------------------------------------------------------------------
@login_required
def alimentacion_listar(request, cultivo_id):
    cultivo = get_object_or_404(Cultivo, id=cultivo_id)
    alimentacion_list = Alimentacion.objects.filter(cultivo=cultivo_id)
    for alimentacion in alimentacion_list:
        if alimentacion.racion_set.count() == 0:
            alimentacion.delete()
    alimentacion_list = Alimentacion.objects.filter(cultivo=cultivo_id)
    return render(request, 'control/alimentacion_list.html',
                  {'alimentacion_list': alimentacion_list, 'cultivo': cultivo})


@login_required
def alimentacion_registrar(request, cultivo_id):  # ración
    hoy = datetime.today().date()
    cultivo = get_object_or_404(Cultivo, id=cultivo_id)
    form = AlimentacionForm()
    try:
        alimentacion = Alimentacion.objects.get(dia=hoy, cultivo=cultivo)
    except Alimentacion.DoesNotExist:
        alimentacion = Alimentacion.objects.create(dia=hoy, cultivo=cultivo)

    if request.method == 'POST':
        form = AlimentacionForm(request.POST)
        if form.is_valid:
            f = form.save(commit=False)
            cantidad_gr = form.cleaned_data['cantidad_gr']
            tipo_concentrado = form.cleaned_data['tipo_concentrado']
            f.cantidad_gr = cantidad_gr
            f.tipo_concentrado = tipo_concentrado
            f.responsable = request.user
            f.alimentacion = alimentacion
            f.save()
            concentrado = Concentrado.objects.get(finca=cultivo.finca, nombre=tipo_concentrado)
            concentrado.total_kg = concentrado.total_kg - (cantidad_gr/1000)
            concentrado.save()
            messages.info(request, 'ración registrada.')
            return redirect('cultivo_list')
    return render(request, 'control/racion.html', {'form': form, 'alimentacion': alimentacion, 'cultivo': cultivo})


@login_required
def alimentacion_editar(request, cultivo_id, alimentacion_id):
    pass


# ----calidad agua------------------------------------------------------------------------------------------------------
@login_required
def calidad_agua_listar(request, estanque_id):
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    calidad_agua_list = Calidad_agua.objects.filter(estanque_id=estanque_id)

    if request.method == 'POST':
        if request.POST['desde'] is (None or "") and request.POST['hasta'] is not (None or ""):  # 0->x
            fecha_top = datetime.strptime(request.POST.get('hasta'), '%d/%m/%Y')
            if fecha_top.date() < calidad_agua_list.first().fecha_registro.date():
                messages.info(request, 'fecha fuera de rango')
            else:
                fecha_topt = datetime.combine(fecha_top, datetime.max.time()).replace(tzinfo=pytz.UTC)
                calidad_agua_list = calidad_agua_list.filter(fecha_registro__lte=fecha_topt)

        if request.POST['desde'] is not (None or "") and request.POST['hasta'] is (None or ""):  # x->fin
            fecha_bot = datetime.strptime(request.POST.get('desde'), '%d/%m/%Y')
            if fecha_bot.date() > calidad_agua_list.last().fecha_registro.date():
                messages.info(request, 'fecha fuera de rango')
            else:
                fecha_bot = fecha_bot.replace(tzinfo=pytz.UTC)
                calidad_agua_list = calidad_agua_list.filter(fecha_registro__gte=fecha_bot)

        if request.POST['desde'] is not (None or "") and request.POST['hasta'] is not (None or ""):  # x->y
            fecha_top = datetime.strptime(request.POST.get('hasta'), '%d/%m/%Y')
            fecha_bot = datetime.strptime(request.POST.get('desde'), '%d/%m/%Y')
            if fecha_top.date() < fecha_bot.date() or fecha_top.date() < calidad_agua_list.first().fecha_registro.date():
                messages.info(request, 'error de rango')
            else:
                fecha_topt = datetime.combine(fecha_top, datetime.max.time()).replace(tzinfo=pytz.UTC)
                fecha_bot = fecha_bot.replace(tzinfo=pytz.UTC)
                calidad_agua_list = calidad_agua_list.filter(fecha_registro__range=(fecha_bot, fecha_topt))

    context = {
        'estanque': estanque,
        'caliagua_list': calidad_agua_list.order_by('-fecha_registro')
    }
    return render(request, 'control/calidad_agua_list.html', context)


@login_required
def calidad_agua_registrar(request, estanque_id):
    form = CalidadAguaForm()
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    if request.method == 'POST':
        form = CalidadAguaForm(request.POST)
        if form.is_valid():
            caliagua = form.save(commit=False)
            caliagua.estanque = estanque
            caliagua.responsable = request.user
            caliagua.save()
            return redirect('estanque_detalle', estanque_id)
    return render(request, 'control/calidad_agua_registrar.html', {'form': form, 'estanque': estanque})


@login_required
def calidad_agua_editar(request, estanque_id, calidad_agua_id):
    caliagua = get_object_or_404(Calidad_agua, pk=calidad_agua_id)
    form = CalidadAguaForm(request.POST or None, instance=caliagua)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('control:calidad_agua_listar', estanque_id)
    return render(request, 'control/calidad_agua_registrar.html', {"form": form})


@login_required
def calidad_agua_detalle(request, estanque_id, calidad_agua_id):
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    caliagua = get_object_or_404(Calidad_agua, pk=calidad_agua_id)
    return render(request, 'control/calidad_agua_detalle.html', {"caliagua": caliagua, "estanque": estanque})


@login_required
def graficas_agua(request, estanque_id):
    estanque = get_object_or_404(Estanque, pk=estanque_id)
    cali_agua = Calidad_agua.objects.filter(estanque=estanque)
    fechas = []
    oxigeno = []
    temperatura = []
    ph = []
    for c_a in cali_agua:
        oxigeno.append(float(c_a.oxigeno))
        fechas.append(c_a.fecha_registro.strftime('%d-%m-%Y'))
        temperatura.append(float(c_a.temperatura))
        ph.append(float(c_a.ph))

    context = {
        "estanque": estanque,
        "object_list": cali_agua,
        "oxigeno": oxigeno,
        "fechas": fechas,
        "temperatura": temperatura,
        "ph": ph,
    }
    return render(request, 'control/graficas_agua.html', context)
