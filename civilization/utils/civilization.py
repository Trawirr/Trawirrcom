from civilization.models import *
from civilization.utils.models_utils import hex_color
import random

def generate_name():
    path = 'static/names/T1.txt'
    used_names = Civilization.objects.values_list('name', flat=True)
    with open(path, 'r') as f:
        names = [n.strip() for n in f.readlines()]
    name = random.choice(names)
    while name in used_names:
        name = random.choice(names)
    return name

def get_tribe_color():
    r, g, b = 0, 0, 0
    while not check_color_correct((r, g, b)):
        r, g, b = (random.randint(0, 255) for i in range(3))
    return ''.join([hex_color(c) for c in (r, g, b)])

def check_color_correct(color):
    if sum(color) < 350:
        return False
    colors = list(Civilization.objects.values_list('color', flat=True))
    if not colors:
        return True

    for other_color in colors:
        other_color_values = split_rgb(other_color)
        diff_color = [abs(color[i] - convert_hex2dec(other_color_values[i])) for i in range(3)]
    return sum(diff_color) > 50

def create_tribes(num_tribes):
    size = max(Tile.objects.values_list('x', flat=True))
    tribes = []
    while num_tribes:
        x_random, y_random = random.randint(0, size), random.randint(0, size)
        if Tile.objects.get(x=x_random, y=y_random).tile_type == "L" and random.random() < .5:
            new_tribe = Civilization(name=generate_name(), color=get_tribe_color())
            new_tribe.save()
            tile = Tile.objects.get(x=x_random, y=y_random)
            tile.owner = new_tribe
            tile.save()
            #print(f"{generate_name()} ({x_random}, {y_random}), color: {get_tribe_color()}")
            num_tribes -= 1