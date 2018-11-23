from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('piscicola/', la_piscicola, name='la_piscicola'),
    path('estanques/', estanque_list, name='estanque_list'),
    path('cultivos/', cultivo_list, name='cultivo_list'),
    path('pagina_error', pagina_error, name='pagina_error'),
    path('siembra',cultivo_siembra, name='siembra')

]