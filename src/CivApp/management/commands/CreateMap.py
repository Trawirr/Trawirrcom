from django.core.management.base import BaseCommand

from PIL import Image

import random

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def add_arguments(self, parser):
        # map parameters
        parser.add_argument('-s', '--size', type=int, default=128, help='Size of a map')
        parser.add_argument('-o', '--octaves', type=str, default="3 6 12 24", help='List of octaves')
        parser.add_argument('-sl', '--sealevel', type=float, default=0.5, help='Sea level/procentage')
        parser.add_argument('-b', '--border', type=int, default=20, help='Border width')
        parser.add_argument('-sd', '--seed', type=int, default=random.randint(1, 100000), help='Map seed')
        parser.add_argument('-n', '--name', type=str, default="map", help='Map file name')
        parser.add_argument('-u', '--username', type=str, default="root", help='Username generating a map')

    def handle(self, *args, **options):
        print("Creating a map...")