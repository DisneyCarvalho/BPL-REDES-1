


from django.contrib import admin
from django.urls import path , include

from . import views

urlpatterns = [
    path('', views.Aplication.as_view() ),
    path('boton/',views.boton.as_view(), name='save'),
    path('getdata/',views.get_data, name='get_data')

]
