from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm # , UserUpdateForm, ProfileUpdateForm
from registro.models import Finca


# Python Django Tutorial: Full-Featured Web App Part 6 - User Registration
def registrar(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST or None)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'registro de {} exitoso!'.format(username))
            return redirect('inicio')
    else:
        # form = UserCreationForm()
        form = UserRegisterForm
    return render(request, 'users/registro.html',{'form': form})

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error

@login_required
def perfil(request):
    try:
        la_pisciola = request.user.profile.trabaja_en
    except:
        la_pisciola = None
    context={
        'la_piscicola': la_pisciola
    }
    return render(request, 'users/perfil.html', context)

    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, 'tu perfil ha actualizado')
    #         return redirect('perfil')
    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)
    # try:
    #     finca = Finca.objects.get(usuarios=request.user)
    # except Finca.DoesNotExist:
    #     finca = None
    #
    # context={
    #      'la_piscicola': finca,
    #      'u_form': u_form,
    #      'p_form': p_form
    # }
    #
    # print(request.user.groups.all)
    # return render(request, 'users/perfil.html', context)




