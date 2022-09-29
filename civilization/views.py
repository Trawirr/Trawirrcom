from django.http import HttpResponse
from django.template import loader
from .models import *

def index(request, map_mode):
    template = loader.get_template('civilization.html')

    tiles = Tile.objects.all()
    tiles = [Tile.objects.filter(y=y) for y in Tile.objects.values_list('y', flat=True).distinct()]

    context = {
        'tiles': tiles,
        'mode': map_mode,
    }
    return HttpResponse(template.render(context, request))