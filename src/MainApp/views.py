from django.shortcuts import render
from .models import Card

def home_view(request):
    return render(request, "pages/home/home.html", {})

def cards_view(request):
    page = int(request.GET.get('page', 0))
    cards = Card.objects.all()
    cards_count = cards.count()
    pages_available = 1 + cards_count - 3
    page_prev = (page - 1) % cards_count
    page_next = (page + 1) % cards_count

    cards_selected = [cards[(page + i) % cards_count] for i in range(3)]

    context = {
        'cards': cards,
        'cards_selected': cards_selected,
        'page_prev': page_prev,
        'page_next': page_next,
    }
    print(f"{context=}")
    return render(request, "pages/home/cards.html", context)

def about_me_view(request):
    return render(request, "pages/home/about_me.html", {})