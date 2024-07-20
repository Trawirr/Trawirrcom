from django.shortcuts import render

def civ_home_view(request):
    return render(request, "pages/civ/civ_home.html", {})

def civ_map_view(request):
    x = request.GET.get('x', 0)
    y = request.GET.get('y', 0)
    zoom = request.GET.get('zoom', 0)
    content = {
        'x': x,
        'y': y,
        'zoom': zoom,
    }
    return render(request, "pages/civ/civ_map.html", content)