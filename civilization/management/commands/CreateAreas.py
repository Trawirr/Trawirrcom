from django.core.management.base import BaseCommand, CommandError
from civilization.utils.map import *

class Command(BaseCommand):
    help = 'Creates new Areas'

    def handle(self, *args, **options):
        # print('Generating land areas...')
        # land_areas = get_separate_areas('type', 'L')
        # create_areas(land_areas, 250, 'I', 'C')

        # print('\nGenerating water areas...')
        # water_areas = get_separate_areas('type', 'W')
        # create_areas(water_areas, 120, 'L', 'S')

        # print('\nGenerating mountain areas...')
        # mountain_areas = get_separate_areas('height', .4, 'higher')
        # create_areas(mountain_areas, 0, 'M', 'M')

        print('Generating rivers and lakes...')
        rivers, lakes = create_rivers(5)
        print(f"{len(rivers)} rivers, {len(lakes)} lakes")
        x = input()
        if x == 'ok':
            for river in rivers:
                for tile in river:
                    tile.tile_type = 'W'
                    tile.save()
            for lake in lakes:
                for tile in lake:
                    tile.tile_type = 'W'
                    tile.save()

        # print('Land > .0')
        # areas = get_separate_areas('height', .0, "higher")
        # for area in areas:
        #     name = generate_name('I') if len(area) < 250 else generate_name('C')
        #     print(len(area), area[0].x, area[0].y, name)
        # print('Land > .0')
        # areas = get_separate_areas('height', .4, "higher")
        # for area in areas:
        #     name = generate_name('I') if len(area) < 250 else generate_name('M')
        #     print(len(area), area[0].x, area[0].y, name)
        # print('\nWater')
        # areas = get_separate_areas('type', 'W',)
        # for area in areas:
        #     print(len(area))

        # print("Generating sources...")
        # create_sources(10)

        # print("Generating tribes...")
        # create_tribes(10)

        # rivers, lakes = create_rivers(5)
        # print(f"{len(rivers)} rivers, {len(lakes)} lakes")
        # x = input()
        # if x == 'ok':
        #     for river in rivers:
        #         for tile in river:
        #             tile.tile_type = 'W'
        #             tile.save()
        #     for lake in lakes:
        #         for tile in lake:
        #             tile.tile_type = 'W'
        #             tile.save()