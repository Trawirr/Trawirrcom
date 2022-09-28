from django.core.management.base import BaseCommand, CommandError
from perlin_noise import PerlinNoise

from civilization.models import *
from civilization.utils.map import *

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def handle(self, *args, **options):
        Tile.objects.all().delete()
        octaves = [3, 6, 16, 24]
        size = 100
        noises = [PerlinNoise(octaves=n) for n in octaves]
        for x in range(size):
            for y in range(size):
                noise_val = 0
                for n, noise in enumerate(noises):
                    noise_val += noise([x/50, y/50]) * .5**n
                noise_val = max(-1.0, min(1.0, (noise_val)) - max(.0, distance(x, y, size)-.8)*2)
                new_tile = Tile(x=x, y=y, height=noise_val, owner=None)
                if noise_val < 0:
                    new_tile.tile_type = 'W'
                new_tile.save()