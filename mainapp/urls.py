from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_article', views.add_article, name='add_article'),
    path('article/<int:article_id>', views.article, name='article'),
]