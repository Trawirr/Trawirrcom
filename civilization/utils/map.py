from unicodedata import numeric
from civilization.models import *
import random
import os
import re

def distance(x, y, size):
    return ((x - size/2)**2 + (y - size/2)**2)**.5/(size/2) 
    #return min(1, (size+size)/6/((size/2 - x)**2 + (size/2 - y)**2 + 1/64)**.5)

def get_tiles_by_height(condition, value):
    if condition == "higher":
        return Tile.objects.filter(height__gte=value)
    elif condition == "lower":
        return Tile.objects.filter(height__lte=value)

def get_tiles_by_type(value):
    return Tile.objects.filter(tile_type=value)

def get_adjacent_tiles(x, y):
    coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    adjacent_tiles = []
    for new_x, new_y in coords:
        try:
            adjacent_tiles.append(Tile.objects.get(x=new_x, y=new_y))
        except:
            pass
    return adjacent_tiles

def get_all_adjacent_tiles(x, y):
    coords = [(x+dx, y+dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
    adjacent_tiles = []
    for new_x, new_y in coords:
        try:
            adjacent_tiles.append(Tile.objects.get(x=new_x, y=new_y))
        except:
            pass
    return adjacent_tiles

def get_lowest_adjacent_tile(x, y):
    adjacent_tiles = get_adjacent_tiles(x, y)
    adjacent_tiles_sorted = sorted(adjacent_tiles, key=lambda t: t.height)
    lowest_adjacent_tile = adjacent_tiles_sorted[0]
    if lowest_adjacent_tile.height < Tile.objects.get(x=x, y=y).height:
        return lowest_adjacent_tile
    return None

def get_separate_areas(mode, value, condition=None, adjacency="simple"):
    if mode == "height":
        all_tiles = list(get_tiles_by_height(condition, value))
    elif mode == "type":
        all_tiles = list(get_tiles_by_type(value))
    areas = []
    while all_tiles:
        to_visit = [all_tiles[0]]
        area_tiles = []
        while to_visit:
            tile = to_visit.pop(0)
            if tile in all_tiles:
                all_tiles.remove(tile)
                area_tiles.append(tile)
                if adjacency == "simple":
                    adjacent_tiles = get_adjacent_tiles(tile.x, tile.y)
                elif adjacency == "full":
                    adjacent_tiles = get_all_adjacent_tiles(tile.x, tile.y)
                for tile in adjacent_tiles:
                    to_visit.append(tile)
        areas.append(area_tiles)
    return areas

# Creating random area names
def get_name_components(area_type):
    path = 'static/names/'
    all_files = os.listdir(path)
    filtered_files = list(filter(lambda f: os.path.isfile(os.path.join(path, f)) and area_type in f, all_files))
    components = []
    for file in filtered_files:
        with open(os.path.join(path, file), 'r') as f:
            words = [word.strip() for word in f.readlines()]
            components.append(words)
    return components

def generate_name(area_type):
    components = get_name_components(area_type)
    while True:
        words = [random.choice(w) for w in components]
        name = ' '.join(words)
        if not is_name_used(area_type, name):
            return name

def is_name_used(area_type, name):
    names = Area.objects.filter(area_type=area_type).values_list('name', flat=True)
    return name in names

# Creating sources in random places
# More probability for creating sources in higher places
# Minimal distance of 5 tiles between each two sources
def create_sources(num_sources):
    size = max(Tile.objects.values_list('x', flat=True))
    sources = []
    while num_sources:
        tile = Tile.objects.get(x=random.randint(0, size), y=random.randint(0, size))
        if random.random() < tile.height and not list(filter(lambda t: abs(tile.x - t.x) + abs(tile.y - t.y) < 5, sources)):
            sources.append(tile)
            num_sources -= 1
    return sources

# TODO
# tworzenie rzek jako Area
def create_rivers(num_sources):
    sources = create_sources(num_sources)
    print(f"Creating rivers... sources: {sources}")
    rivers = []
    lakes = []
    for source in sources:
        tile = source
        river_tiles = []
        while tile and tile.tile_type != 'W':
           river_tiles.append(tile)
           print(f"{len(river_tiles)}. ({tile.x}, {tile.y})")
           tile = get_lowest_adjacent_tile(tile.x, tile.y)
        rivers.append(river_tiles)
        
        # Creating a lake
        if not tile:
            lake_tiles = create_lake(river_tiles[-1], river_tiles[-2].height)
            lakes.append(lake_tiles)
            print("\nLake tiles:")
            for i, t in enumerate(lake_tiles):
                print(f"{i}. ({t.x}, {t.y})")
        print()
    return rivers, lakes

def create_lake(start_tile, height, max_size_constraints=(3,8)):
    all_tiles = list(get_tiles_by_height("lower", height))
    height = (start_tile.height + height) / 2
    lake_tiles = []
    to_visit = [start_tile]
    max_size = random.randint(max_size_constraints[0], max_size_constraints[1])
    while to_visit and len(lake_tiles) < max_size:
        tile = to_visit.pop(0)
        if tile in all_tiles:
            all_tiles.remove(tile)
            try:
                if not list(filter(lambda t: t.tile_type == "W", get_adjacent_tiles(tile.x, tile.y))):
                    lake_tiles.append(tile)
                    for tile in get_adjacent_tiles(tile.x, tile.y):
                        to_visit.append(tile)
                else:
                    print(f"({tile.x}, {tile.y}) adjacent to water, {len(to_visit)} tiles to check")
            except Exception as e:
                print(e)
    return lake_tiles

def create_land_areas():
    areas = get_separate_areas('type', 'L', adjacency="full")
    for area in areas:
        if len(area) < 250:
            new_area = Area(name=generate_name('I'), area_type='I')
            new_area.save()
            print(f"New area ({new_area.get_area_type_display()} {new_area.name}) created")
            for tile in area:
                tile.areas.add(new_area)
            print(f"{len(area)} tiles added")
        else:
            new_area = Area(name=generate_name('C'), area_type='C')
            new_area.save()
            print(f"New area ({new_area.get_area_type_display()} {new_area.name}) created")
            for tile in area:
                tile.areas.add(new_area)
            print(f"{len(area)} tiles added")

def create_areas(areas, threshold, type1, type2):
    for area in areas:
        if len(area) < threshold:
            new_area = Area(name=generate_name(type1), area_type=type1)
            new_area.save()
            print(f"New area ({new_area.area_type} {new_area.name}) created")
            for tile in area:
                tile.areas.add(new_area)
            print(f"{len(area)} tiles added")
        else:
            new_area = Area(name=generate_name(type2), area_type=type2)
            new_area.save()
            print(f"New area ({new_area.area_type} {new_area.name}) created")
            for tile in area:
                tile.areas.add(new_area)
            print(f"{len(area)} tiles added")

# Creating resources
def create_resources(num_resources):
    all_tiles = Tile.objects.filter(tile_type='L')
    all_resources = Resource.objects.all()
    resources = []
    while num_resources:
        resource_random = random.choice(all_resources)
        tile_random = random.choice(all_tiles)
        #print(f"{tile_random.height} height, {resource_random.production} production, {resource_random.food} food")
        # production resource
        if resource_random.production > resource_random.food:
            #if random.random() < tile_random.height - (resource_random.production - resource_random.culture)/20:
            if random.random() < tile_random.height * resource_random.production + resource_random.culture/30:
                print(f'    Resource created - {resource_random.name} on {tile_random.height_m}m')
                num_resources -= 1
                resources.append((tile_random, resource_random))
        #elif random.random() < 0.5 - tile_random.height - (resource_random.food - resource_random.culture)/20:
        elif random.random() < (0.25 - tile_random.height) * resource_random.food + resource_random.culture/30:
            print(f'    Resource created - {resource_random.name} on {tile_random.height_m}m')
            num_resources -= 1
            resources.append((tile_random, resource_random))
    for r in Resource.objects.values_list('name', flat=True):
        print(f"{r}: {[r.name for _, r in resources].count(r)}")
    decision = input('resources ok?')
    if decision == 'ok':
        for tile, resource in resources:
            tile.resource = resource
            tile.save()
