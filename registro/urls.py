from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('piscicola/', la_piscicola, name='la_piscicola'),
    path('<int:piscicola_id>/estanques/', estanque_list, name='estanque_list'),
    path('<int:piscicola_id>/cultivos/', cultivo_list, name='cultivo_list'),
    path('pagina_error', pagina_error, name='pagina_error'),
]