from django.core.management.base import BaseCommand, CommandError

from civilization.models import *

class Command(BaseCommand):
    help = 'Creates a backup for tiles'

    def handle(self, *args, **options):
        tiles = Tile.objects.all()
        with open("tiles.txt", "w") as f:
            for tile in tiles:
                f.write(f"{tile.x}, {tile.y}, {tile.height}\n")