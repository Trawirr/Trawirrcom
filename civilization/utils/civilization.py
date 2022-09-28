from civilization.models import *
import random

def create_tribes(num_tribes):
    size = max(Tile.objects.values_list('x', flat=True))
    sources = []
    while num_tribes:
        x_random, y_random = random.randint(0, size), random.randint(0, size)
        if Tile.objects.get(x=x_random, y=y_random).tile_type == "L" and random.random() < .5:
            print(f"Tribe ({x_random}, {y_random})")
            num_tribes -= 1