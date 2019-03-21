from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ConcentradoForm, CompraBultosForm
from .models import Concentrado, CompradeBultos


# Create your views here.
@login_required
def concentrado_list(request):
    concentrados = Concentrado.objects.filter(finca=request.user.profile.trabaja_en)
    context = {
        'concentrados': concentrados
    }
    return render(request, 'inventario/concentrado_list.html', context)


@login_required
def concentrado_create(request):
    if request.method == 'POST':
        form = ConcentradoForm(request.POST or None)
        if form.is_valid():
            concentrado = form.save(commit=False)
            concentrado.finca = request.user.profile.trabaja_en
            concentrado.responsable = request.user
            concentrado.save()
            return redirect('inventario:concentrado_list')
    else:
        form = ConcentradoForm()
    context = {
        'form': form,
    }
    return render(request, 'inventario/concentrado_create.html', context)

@login_required
def compra_bultos_create(request):
    if request.method == 'POST':
        form = CompraBultosForm(request.POST or None)
        if form.is_valid():
            bultos = form.cleaned_data['numero_bultos']
            tipo_concentrado = form.cleaned_data['concentrado']
            compra = form.save(commit=False)
            compra.finca = request.user.profile.trabaja_en
            compra.responsable = request.user
            compra.save()
            concentrado = Concentrado.objects.get(finca=request.user.profile.trabaja_en, nombre=tipo_concentrado)
            concentrado.total_kg = concentrado.total_kg + (bultos*concentrado.kilos)
            concentrado.save()
            return redirect('inventario:concentrado_list')
    else:
        form = CompraBultosForm()
    context = {
        'form': form,
    }
    return render(request, 'inventario/compra_bultos_create.html', context)


@login_required
def compra_bultos_list(request):
    concentrado_comprado = CompradeBultos.objects.filter(finca=request.user.profile.trabaja_en)
    context = {
        'concentrado_comprado': concentrado_comprado
    }
    return render(request, 'inventario/compra_bultos_list.html', context)

