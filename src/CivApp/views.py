from django.shortcuts import render

def civ_home_view(request):
    return render(request, "pages/civ/civ_home.html", {})