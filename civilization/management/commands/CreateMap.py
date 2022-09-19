from django.core.management.base import BaseCommand, CommandError
from BorsukUlam.utils.borsukulam import *

from civilization.models import *
from civilization.utils.civilization import *

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def handle(self, *args, **options):
        Tile.objects.all().delete()
        for x in range(40):
            for y in range(40):
                new_tile = Tile(x=x, y=y, height=5, color=decimal_hex((x+y)), owner=None)
                new_tile.save()