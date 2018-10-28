from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
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
            # form.save()
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
    finca = Finca.objects.get(usuarios=request.user)
    context = {
        'la_piscicola': finca
    }
    print(request.user.groups.all)
    return render(request, 'users/perfil.html', context)




