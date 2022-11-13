from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sensitivity', views.sensitivity, name='sensitivity'),
    path('observtime', views.observtime, name='observing time'),
]
