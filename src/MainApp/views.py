from django.shortcuts import render
from .models import Card

def home_view(request):
    return render(request, "pages/home.html", {})

def cards_view(request):
    context = {
        'cards': Card.objects.all(),
    }
    print(f"{context=}")
    return render(request, "pages/cards.html", context)