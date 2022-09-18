from django.core.management.base import BaseCommand, CommandError
from BorsukUlam.utils.borsukulam import *

from civilization.models import *

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def handle(self, *args, **options):
        for x in range(5):
            for y in range(5):
                new_tile = Tile(x=x, y=y, height=5, color=150, owner=None)
                new_tile.save()