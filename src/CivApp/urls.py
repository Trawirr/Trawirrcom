from django.urls import path
from . import views

urlpatterns = [
    path('', views.civ_home_view, name='civilization-home'),
]