from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cards', views.cards_view, name='cards'),
    path('about-me', views.about_me_view, name='about-me'),
]