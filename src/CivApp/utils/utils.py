from perlin_noise import PerlinNoise
import numpy as np

HEIGHTS_WATER = (
    0.05,
    0.2,
    0.7,
    0.95,
    1.0
)

COLORS_WATER = (
    (0, 0, 50),
    (25, 100, 140),
    (35, 145, 200),
    (45, 175, 255),
    (45, 190, 255)
)

HEIGHTS_LAND = (
    0.1,
    0.3,
    0.5,
    0.65,
    0.8,
    1.0
)

COLORS_LAND = (
    (114, 193, 134),
    (162, 215, 164),
    (225, 227, 158),
    (241, 151, 82),
    (221, 100, 80),
    (130, 40, 23)
)

def get_cylindrical_coordinates(x, y, width, height, distance_between_points=0.01):
    radius = width * distance_between_points / (2 * np.pi)

    x_cyl = radius * np.cos(2 * np.pi * x / width)
    y_cyl = radius * np.sin(2 * np.pi * x / width)
    z_cyl = y * distance_between_points
    return x_cyl, y_cyl, z_cyl

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def distance_from_border(pos, size):
    return min(pos, size + 1 - pos)

def map_value(value, min1, max1, min2, max2):
    value = max(min(value, max1), min1)
    span1 = max1 - min1
    span2 = max2 - min2

    value_scaled = float(value - min1) / float(span1)

    return min2 + (value_scaled * span2)

def get_height(x, y, octaves, seed, width, height, border):
    limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
    noises = [PerlinNoise(octaves=o, seed=seed) for o in octaves]
    height = 0
    for i, noise in enumerate(noises):
        height += noise([x/100, y/100]) * .5**i
    return height

def get_height3(x, y, z, octaves, seed):
    noises = [PerlinNoise(octaves=o, seed=seed) for o in octaves]
    height = 0
    for i, noise in enumerate(noises):
        height += noise([x, y, z]) * .5**i

    return height

def fix_height(tile_height, x, y, height, border, seed):
    if border > 0:
        noise = PerlinNoise(octaves=2, seed=seed)
        distance = distance_from_border(y, height)
        if distance == 1 and tile_height >= 0:
            tile_height *= -0.1 * abs(noise([x/100]))
        elif distance <= border and tile_height >= 0:
            tile_height *= map_value(distance, 1, border, 0, 1)
    return tile_height

def fix_height2(tile_height, x, y, height, border, seed):
    if border > 0:
        noise = PerlinNoise(octaves=2, seed=seed)
        distance = distance_from_border(y, height)
        if distance <= border and tile_height >= 0:
            tile_height = map_value(distance, 1, border, -tile_height, tile_height)
    return tile_height

def fix_height3(tile_height, x, y, height, border, seed):
    if border > 0:
        noise = PerlinNoise(octaves=2, seed=seed)
        distance = distance_from_border(y, height)
        if distance <= border:
            tile_height = map_value(distance, 1, border, -1, tile_height)
    return tile_height

def fix_height4(tile_height, x, y, height, border, seed):
    if border > 0:
        noise = PerlinNoise(octaves=2, seed=seed)
        distance = distance_from_border(y, height)
        if distance <= border:
            tile_height = map_value(distance, 1, border, -abs(noise([x/100])), tile_height)
    return tile_height

def fix_height5(tile_height, x, y, width, height, border, seed, octaves):
    x_cyl, y_cyl, z_cyl = get_cylindrical_coordinates(x, y, width, height)
    if border > 0:
        distance = distance_from_border(y, height)
        if distance <= border:
            tile_height2 = get_height3(x_cyl, y_cyl + seed, z_cyl, octaves, seed)
            tile_height = map_value(distance, 1, border, -abs(tile_height2), tile_height)
    return tile_height

def calculate_height(tile_height: float, x: int, y: int, width: int, height: int, border: int, seed: int, octaves: list[int], fix_mode: int = 5):
     pass

def get_color(height, tile_type="land"):
    if tile_type == "land":
        heights, colors = HEIGHTS_LAND, COLORS_LAND
    elif tile_type == "water":
        heights, colors = HEIGHTS_WATER, COLORS_WATER
        height += 1

    for i, h in enumerate(heights):
        if h >= height:
            return colors[i]