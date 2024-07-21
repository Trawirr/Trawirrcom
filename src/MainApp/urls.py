from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cards', views.cards_view, name='cards'),
    path('about-me', views.about_me_view, name='about-me'),
    path('1', views.home_view, name='processing-home'),
    path('2', views.home_view, name='gesture-glove-home'),
    path('3', views.home_view, name='borsukulam-home'),
]