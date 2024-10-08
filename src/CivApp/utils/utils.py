from perlin_noise import PerlinNoise
import numpy as np

HEIGHTS_WATER = (
    0.0,
    0.05,
    0.2,
    0.7,
    0.95,
    1.0
)

COLORS_WATER = (
    (0, 0, 0),
    (0, 0, 50),
    (25, 100, 140),
    (35, 145, 200),
    (45, 175, 255),
    (45, 190, 255)
)

HEIGHTS_LAND = (
    0.0,
    0.1,
    0.3,
    0.5,
    0.65,
    0.8,
    1.0
)

COLORS_LAND = (
    (105, 183, 154),
    (114, 193, 134),
    (162, 215, 164),
    (225, 227, 158),
    (241, 151, 82),
    (221, 100, 80),
    (130, 40, 23)
)

BIOME_RULES = [
    #[humidity, temperature]
    [0, 0.8],
    [0.2, 0.0],
    [0.2, 0.4],
    [0.4, -0.2],
    [0.6, 0.6],
    [1, 0.85],
    [0.5, -0.7],
    [0, -0.9]
]

BIOME_NAMES = [
    "Desert",
    "Grassland",
    "Grassland",
    "Forest",
    "Forest",
    "Tropical forest",
    "Boreal forest",
    "Tundra",
]

BIOME_COLORS = [
    (255, 255, 102),
    (204, 255, 153),
    (204, 255, 153),
    (0, 153, 0),
    (0, 153, 0),
    (51, 255, 51),
    (102, 51, 0),
    (204, 255, 255),
]

SHADOW_COLORS = [0, 0, 0]

def densify_array(array: list, factor: int):
    dense_array = []
    for i in range(len(array) - 1):
        for l in np.linspace(array[i], array[i+1], factor, dtype=float, endpoint=False):
            dense_array.append(l)
    dense_array.append(array[-1])
    return dense_array

def convert_height_to_color(height: float, octaves: list[int]):
    limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
    value = int(map_value(height, -limit, limit, 0, 256**3))
    color = [0, 0, 0]
    for i in range(3):
        color[2-i] = int(value % 256)
        value = (value - color[2-i]) / 256
    return tuple(color)

def convert_color_to_height(color: list[int] | tuple[int], octaves: list[int]):
    limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
    exps = [256 ** (2 - i) for i in range(3)]
    value = 0
    for c, e in zip(color, exps):
        value += c * e
    return map_value(value, 0, 256**3, -limit, limit)

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

def fix_height1(tile_height, x, y, height, border, seed):
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

def fix_height(tile_height: float, x: int, y: int, width: int, height: int, border: int, seed: int, octaves: list[int], fix_mode: int = 5):
     fix_height_functions = [fix_height1, fix_height2, fix_height3, fix_height4]
     if fix_mode == 5:
         return fix_height5(tile_height, x, y, width, height, border, seed, octaves)
     else:
         return fix_height_functions[fix_mode-1](tile_height, x, y, height, border, seed)
     
def process_height(tile_height: float):
    # lowering values lower than 0.25
    tile_height = tile_height ** map_value(tile_height, 0, 0.25, 1.5, 1)

    return tile_height

def get_color(height, tile_type="land", smoothing: int = 1):
    if tile_type == "land":
        heights, colors = HEIGHTS_LAND, COLORS_LAND
    elif tile_type == "water":
        heights, colors = HEIGHTS_WATER, COLORS_WATER
        height += 1

    if smoothing > 0:
        heights = densify_array(heights, smoothing)
        colors = densify_array(colors, smoothing)

    for i, h in enumerate(heights):
        if h >= height:
            # print(f"{i=}, {h=}, {height=}, {colors[i]=}, {tile_type=}")
            if smoothing == 0:
                return tuple(int(map_value(height, heights[i-1], heights[i], colors[i-1][c], colors[i][c])) for c in range(3))
            else:
                return tuple(int(c) for c in colors[i])
        
def get_temperature3(x: int, y: int, z: int, seed: int, octave: int = 2):
    return PerlinNoise(octaves=octave, seed=seed)([x, y, z])
        
def get_humidity3(x: int, y: int, z: int, seed: int, octave: int = 3):
    return PerlinNoise(octaves=octave, seed=seed)([x, y, z])

def get_biome_color(temperature: float, humidity: float, biome_coords=BIOME_RULES):
    min_dist = 100
    biome_id = None
    for i, rule in enumerate(biome_coords):
        distance_to_biome = distance(temperature, humidity, rule[0], rule[1])
        if distance_to_biome < min_dist:
            min_dist = distance_to_biome
            biome_id = i
    return BIOME_COLORS[biome_id]

def is_on_edge(x: int, y: int, width: int, height: int):
    if x == 0 or y == 0:
        return True
    if x == width - 1 or y == height - 1:
        return True
    return False

def is_on_horizontal_edge(y: int, height: int):
    return is_on_edge(1, y, 3, height)

def get_shadow_color(height: float, height_adj: float):
    return tuple(SHADOW_COLORS + [int(map_value(height_adj - height, 0, 0.2, 0, 100))])