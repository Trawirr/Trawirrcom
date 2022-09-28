from venv import create
from django.core.management.base import BaseCommand, CommandError
from civilization.utils.map import *

class Command(BaseCommand):
    help = 'Creates new Resources'

    def handle(self, *args, **options):
        print('Creating resources...')
        create_resources(50)