from civilization.models import *
import random

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

def get_lowest_adjacent_tile(x, y):
    adjacent_tiles = get_adjacent_tiles(x, y)
    adjacent_tiles_sorted = sorted(adjacent_tiles, key=lambda t: t.height)
    lowest_adjacent_tile = adjacent_tiles_sorted[0]
    if lowest_adjacent_tile.height < Tile.objects.get(x=x, y=y).height:
        return lowest_adjacent_tile
    return None

def get_separate_areas(mode, value, condition=None):
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
                for tile in get_adjacent_tiles(tile.x, tile.y):
                    to_visit.append(tile)
        areas.append(area_tiles)
    return areas

# Creating sources in random places
# More probability for creating sources in higher places
# Minimal distance of 5 tiles between each two sources
def create_sources(num_sources):
    size = max(Tile.objects.values_list('x', flat=True))
    sources = []
    while num_sources:
        tile = Tile.objects.get(x=random.randint(0, size), y=random.randint(0, size))
        if random.random() < tile.height and not list(filter(lambda t: abs(tile.x - t.x) + abs(tile.y - t.y) )):
            sources.append(tile)
            num_sources -= 1
    return sources

def create_rivers(num_sources):
    sources = create_sources(num_sources)
    print(f"Creating rivers... sources: {sources}")
    rivers = []
    for source in sources:
        tile = source
        river_tiles = []
        while tile and tile.tile_type != 'W':
           river_tiles.append(tile)
           print(f"{len(river_tiles)}. ({tile.x}, {tile.y})")
           tile = get_lowest_adjacent_tile(tile.x, tile.y)
        rivers.append(river_tiles)
    return rivers

def create_lake(x, y, height):
    pass

def create_tribes(num_tribes):
    size = max(Tile.objects.values_list('x', flat=True))
    sources = []
    while num_tribes:
        x_random, y_random = random.randint(0, size), random.randint(0, size)
        if Tile.objects.get(x=x_random, y=y_random).tile_type == "L" and random.random() < .5:
            print(f"Tribe ({x_random}, {y_random})")
            num_tribes -= 1