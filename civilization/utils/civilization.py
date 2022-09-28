from civilization.models import *
from civilization.utils.models_utils import hex_color
import random

def get_tribe_color():
    r, g, b = 0, 0, 0
    while r+g+b < 300 and check_color_correct((r, g, b)):
        r, g, b = (random.randint(0, 255) for i in range(3))
    return ''.join([hex_color(c) for c in (r, g, b)])

def check_color_correct(color):
    colors = list(Civilization.objects.values_list('color', flat=True))
    for other_color in colors:
        other_color_values = hex_value(other_color)
        diff_color = [abs(color[i] - other_color_values[i]) for i in range(3)]

def create_tribes(num_tribes):
    size = max(Tile.objects.values_list('x', flat=True))
    tribes = []
    while num_tribes:
        x_random, y_random = random.randint(0, size), random.randint(0, size)
        if Tile.objects.get(x=x_random, y=y_random).tile_type == "L" and random.random() < .5:
            print(f"Tribe ({x_random}, {y_random}), color: {get_tribe_color()}")
            num_tribes -= 1