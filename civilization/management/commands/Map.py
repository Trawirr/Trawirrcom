from django.core.management.base import BaseCommand, CommandError

from civilization.models import *

class Command(BaseCommand):
    help = 'Creates a backup for tiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--load',
            action='store_true',
            help='Loading saved map',
        )

        parser.add_argument(
            '--save',
            action='store_true',
            help='Saving map',
        )

    def handle(self, *args, **options):
        if options['save']:
            tiles = Tile.objects.all()
            with open("tiles.txt", "w") as f:
                for tile in tiles:
                    f.write(f"{tile.x}, {tile.y}, {tile.height}\n")
        elif options['load']:
            with open('civilization/management/commands/tiles.txt', 'r') as f:
                tiles = f.readlines()
            Tile.objects.all().delete()
            for tile in tiles:
                x, y, height = tile.strip().split(', ')
                print(100*int(x)+int(y))
                tile_type = "L" if float(height) >= 0.0 else "W"
                new_tile = Tile(x=int(x), y=int(y), height=float(height), tile_type=tile_type, owner=None)
                new_tile.save()
