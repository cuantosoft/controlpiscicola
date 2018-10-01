from django.urls import path
from .views import *



urlpatterns = [
    path('estanques/', estanque_list, name='estanque_list'),
    path('cultivos/', cultivo_list, name='cultivo_list'),
]