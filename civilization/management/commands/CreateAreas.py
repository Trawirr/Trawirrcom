from django.core.management.base import BaseCommand, CommandError
from civilization.utils.civilization import *

class Command(BaseCommand):
    help = 'Creates new Areas'

    def handle(self, *args, **options):
        areas = get_separate_areas("higher", .001)
        for area in areas:
            print(len(area))