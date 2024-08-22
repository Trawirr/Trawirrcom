from perlin_noise import PerlinNoise

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def map_value(value, min1, max1, min2, max2):
    value = max(min(value, max1), min1)
    span1 = max1 - min1
    span2 = max2 - min2

    value_scaled = float(value - min1) / float(span1)

    return min2 + (value_scaled * span2)

def get_height(x, y, octaves, seed, size, border):
    limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
    noises = [PerlinNoise(octaves=o, seed=seed) for o in octaves]
    height = 0
    for i, noise in enumerate(noises):
        height += noise([x/100, y/100]) * .5**i

    if border > 0:
        distance_from_edge = distance(x, y, size//2, size//2) - size//2 + border
        if distance_from_edge > 0:
            height -= map_value(distance_from_edge, 0, border, 0, limit)

    # if height > 0:
    #     height = lower_height(height)
    return height