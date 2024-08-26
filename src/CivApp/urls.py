from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.civ_home_view, name='civilization-home'),
    path('map', views.civ_map_view, name='civilization-map'),
]   