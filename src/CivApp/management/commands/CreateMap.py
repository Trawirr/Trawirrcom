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
        parser.add_argument('-bo', '--biomeoctaves', type=str, default="1 2 5 8 12", help='List of octaves for biome generation')
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
        octaves_biome = options['biomeoctaves']
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
        image_heightmap = Image.new("RGB", (width, height))
        image_rgb = Image.new("RGB", (width, height))
        image_biomes = Image.new("RGB", (width, height))
        image_political = Image.new("RGB", (width, height))

        start = time.time()
        progress = 0
        estimated_time = 0
        for x in range(width):
            for y in range(height):
                x_cyl, y_cyl, z_cyl = get_cylindrical_coordinates(x, y, width, height)

                # elevation map
                tile_height = get_height3(x_cyl, y_cyl, z_cyl, octaves, seed)
                tile_height = fix_height(tile_height, x, y, width, height, border, seed, octaves)
                tile_type = "land" if tile_height >= 0 else "water"

                # biome map
                humidity = get_humidity3(x_cyl, y_cyl, z_cyl, seed)
                temperature = get_temperature3(x_cyl, y_cyl, z_cyl, seed)

                # updating images
                image_heightmap.putpixel((x, y), convert_height_to_color(tile_height, octaves))

                image_rgb.putpixel((x, y), get_color(tile_height, tile_type))

                if tile_type == "land": image_political.putpixel((x, y), (255, 255, 255))
                else: image_political.putpixel((x, y), get_color(tile_height, tile_type))

                if tile_type == "land": image_biomes.putpixel((x, y), get_biome_color(temperature, humidity))
                else: image_political.putpixel((x, y), get_color(tile_height, tile_type))

                # displaying progress
                progress += 1
                estimated_time = (time.time() - start) / progress * (width * height - progress)
                done_tenth = int(progress / (width * height) * 10)
                print(f"Progress: [{'#' * done_tenth}{'.' * (10 - done_tenth)}] {progress / (width * height) * 100:.2f}%, estimated time: {estimated_time:.0f}s   ", end='\r')

        image_heightmap.save(settings.MEDIA_ROOT / f"civ_maps/{name}_heightmap.png")
        image_rgb.save(settings.MEDIA_ROOT / f"civ_maps/{name}.png")
        image_political.save(settings.MEDIA_ROOT / f"civ_maps/{name}_political.png")
        image_biomes.save(settings.MEDIA_ROOT / f"civ_maps/{name}_biomes.png")
        print("\ndone")