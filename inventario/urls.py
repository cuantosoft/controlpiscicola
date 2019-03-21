from django.urls import path
from .views import *

app_name = 'inventario'

urlpatterns = [
    path('concentrado/', concentrado_list, name='concentrado_list'),
    path('concentrado/nuevo/', concentrado_create, name='concentrado_create'),
    path('concentrado/comprabultos/nuevo/', compra_bultos_create, name='compra_bultos_create'),
    path('concentrado/comprabultos/', compra_bultos_list, name='compra_bultos_list'),
]
