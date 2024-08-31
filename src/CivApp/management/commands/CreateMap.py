from django.core.management.base import BaseCommand
from django.conf import settings
from CivApp.models import Map
from CivApp.utils.utils import *

from PIL import Image

import random
import time

class Command(BaseCommand):
    help = 'Creates a new map'

    def add_arguments(self, parser):
        # Map parameters
        parser.add_argument('size', metavar='s', type=int, nargs='+', help='Two integers: width height')
        parser.add_argument('-o', '--octaves', type=str, default="1 2 5 8 12", help='List of octaves')
        parser.add_argument('-sl', '--sealevel', type=float, default=0.5, help='Sea level/procentage')
        parser.add_argument('-b', '--border', type=int, default=20, help='Vertical border width')
        parser.add_argument('-m', '--margin', type=int, default=20, help='Margin describing shape of borders')
        parser.add_argument('-sd', '--seed', type=int, default=random.randint(1, 100000), help='Map seed')
        parser.add_argument('-n', '--name', type=str, default="map", help='Map file name')

    def handle(self, *args, **options):
        print("Creating a map...")
        # Fetch options
        width, height = options['size']
        octaves = options['octaves']
        sea_level_arg = options['sealevel']
        border = options['border']
        margin = options['margin']
        seed = options['seed']
        name = options['name']

        # Handle wrong values
        if border > height // 2:
            print(f"Warning: wrong values of {border=}, changed to {height // 2}")
            border = height // 2
        
        # Prepare images and octaves
        octaves = [int(o) for o in octaves.split()]
        image_heightmap = Image.new("L", (width, height))
        image_rgb = Image.new("RGB", (width, height))
        image_biomes = Image.new("RGB", (width, height))
        image_political = Image.new("RGB", (width, height))

        start = time.time()
        progress = 0
        estimated_time = 0
        for x in range(width):
            for y in range(height):
                x_cyl, y_cyl, z_cyl = get_cylindrical_coordinates(x, y, width, height)
                tile_height = get_height3(x_cyl, y_cyl, z_cyl, octaves, seed)
                tile_height = fix_height(tile_height, x, y, width, height, border, seed, octaves)
                tile_type = "land" if tile_height >= 0 else "water"

                image_rgb.putpixel((x, y), get_color(tile_height, tile_type))
                progress += 1
                estimated_time = (time.time() - start) / progress * (width * height - progress)
                print(f"Progress: {progress / (width * height) * 100:.2f}%, estimated time: {estimated_time:.0f}s   ", end='\r')

        image_rgb.save(settings.MEDIA_ROOT / f"civ_maps/{name}.png")
        print("\ndone")