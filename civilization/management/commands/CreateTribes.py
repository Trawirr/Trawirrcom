from django.core.management.base import BaseCommand, CommandError
from civilization.utils.civilization import *

class Command(BaseCommand):
    help = 'Creates new Areas'

    def handle(self, *args, **options):
        create_tribes(5)