from django.urls import path
from .views import *


urlpatterns = [
    path('piscicola/', la_piscicola, name='la_piscicola'),
    path('cosechas/', cosecha_list, name='cosecha_list'),
    # --------------------------------------------------------------------------------------
    path('estanques/', estanque_list, name='estanque_list'),
    path('estanques/crear/', estanque_crear, name='estanque_crear'),
    path('estanques/<int:estanque_id>/',estanque_detalle, name='estanque_detalle'),
    path('estanques/<int:estanque_id>/editar/', estanque_editar, name='estanque_editar'),
    # --------------------------------------------------------------------------------------
    path('cultivos/', cultivo_list, name='cultivo_list'),
    path('cultivos/crear/',cultivo_crear, name='cultivo_crear'),
    path('cultivos/<int:cultivo_id>/',cultivo_detalle, name='cultivo_detalle'),
    path('cultivos/<int:cultivo_id>/editar/', cultivo_editar, name='cultivo_editar'),
]