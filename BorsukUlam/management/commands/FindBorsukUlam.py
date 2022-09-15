from django.core.management.base import BaseCommand, CommandError
from BorsukUlam.utils.borsukulam import *
from BorsukUlam.models import *

class Command(BaseCommand):
    help = 'Finds a Borsuk-Ulam point'

    def handle(self, *args, **options):
        BorsukUlamPoint.objects.all().delete()
        bu = BorsukUlam()
        info = bu.find_Borsuk_Ulam()
        print(info)