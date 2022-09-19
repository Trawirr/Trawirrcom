from django.core.management.base import BaseCommand, CommandError
from perlin_noise import PerlinNoise

from civilization.models import *
from civilization.utils.civilization import *

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def handle(self, *args, **options):
        Tile.objects.all().delete()
        octaves = [3, 6, 16, 24]
        noises = [PerlinNoise(octaves=n) for n in octaves]
        for x in range(50):
            for y in range(50):
                noise_val = 0
                for n, noise in enumerate(noises):
                    noise_val += noise([x/50, y/50]) * .5**n
                new_tile = Tile(x=x, y=y, height=noise_val, owner=None)
                if noise_val < 0:
                    new_tile.tile_type = 'W'
                new_tile.save()