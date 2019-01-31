from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name ='control'
urlpatterns = [
    path('cultivos/<int:cultivo_id>/muestreos/', muestreo_listar, name='muestreo_listar'),
    path('cultivos/<int:cultivo_id>/muestreos/registrar/', muestreo_registrar, name='muestreo_registrar'),
    path('cultivos/<int:cultivo_id>/muestreos/<int:muestreo_id>/editar/', muestreo_editar, name='muestreo_editar'),
    path('cultivos/<int:cultivo_id>/mortalidad/', mortalidad_registrar, name='mortalidad_registrar'),
    # --------------------------------------------------------------------------------------------------------------
    path('cultivos/<int:cultivo_id>/alimentacion/', alimentacion_listar, name='alimentacion_listar'),
    path('cultivos/<int:cultivo_id>/alimentacion/registrar/', alimentacion_registrar, name='alimentacion_registrar'),
    path('cultivos/<int:cultivo_id>/alimentacion/<int:alimentacion_id>/editar/', alimentacion_editar, name='alimentacion_editar'),
    # --------------------------------------------------------------------------------------------------------------
    path('estanques/<int:estanque_id>/calidad_agua/', calidad_agua_listar, name='calidad_agua_listar'),
    path('estanques/<int:estanque_id>/calidad_agua/registrar/', calidad_agua_registrar, name='calidad_agua_registrar'),
    path('estanques/<int:estanque_id>/calidad_agua/<int:calidad_agua_id>/', calidad_agua_detalle, name='calidad_agua_detalle'),
    path('estanques/<int:estanque_id>/calidad_agua/<int:calidad_agua_id>/editar/', calidad_agua_editar, name='calidad_agua_editar'),
    path('estanques/<int:estanque_id>/calidad_agua/graficas_agua/', graficas_agua, name='graficas_agua'),
]