from django.urls import path
from . import views

urlpatterns = [
    path('borsukulam', views.index, name='index'),
]