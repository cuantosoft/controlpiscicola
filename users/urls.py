from django.urls import path
from users import views as user_views
from django.contrib.auth.decorators import login_required

# Python Django Tutorial: Full-Featured Web App Part 7 - Login and Logout System
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registrar/', user_views.registrar, name='registrar'),
    path('ingresar/', auth_views.LoginView.as_view(template_name='users/ingresar.html'), name='ingresar'),
    path('salir/', auth_views.LogoutView.as_view(template_name='users/salir.html'), name='salir'),
    path('perfil/', user_views.perfil, name='perfil'),
]