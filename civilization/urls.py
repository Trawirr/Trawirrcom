from django.urls import path
from . import views

urlpatterns = [
    path('<str:map_mode>', views.index, name='index'),
]