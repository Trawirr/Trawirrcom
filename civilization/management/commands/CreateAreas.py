from venv import create
from django.core.management.base import BaseCommand, CommandError
from civilization.utils.civilization import *

class Command(BaseCommand):
    help = 'Creates new Areas'

    def handle(self, *args, **options):
        # print('Land > .5')
        # areas = get_separate_areas('height', .5, "higher")
        # for area in areas:
        #     print(len(area))
        # print('\nWater')
        # areas = get_separate_areas('type', 'W',)
        # for area in areas:
        #     print(len(area))

        print("Generating sources...")
        create_sources(10)