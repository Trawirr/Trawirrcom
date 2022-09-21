import numpy as np

WATER_COLORS = [
    [-1.0, np.array([0,0,100])],
    [-.5, np.array([0,0,120])],
    [0, np.array([0,0,255])],
    [1.0, np.array([0,150,255])]
]

LAND_COLORS = [
    [0, np.array([0,215,0])],
    [.3, np.array([220,255,0])],
    [.4, np.array([255,80,0])],
    [.8, np.array([0,0,0])],
    [1.0, np.array([0,0,0])]
]

def decimal_hex(value):
    digits = '0123456789ABCDEF'
    r = digits[value//256]
    value = value%256
    g = digits[value//16]
    b = digits[value%16]
    return r+g+b

def hex_color(value):
    value = int(value)
    digits = '0123456789ABCDEF'
    return f"{digits[value//16]}{digits[value%16]}"

def get_color(colors, height):
    for i, (h, _) in enumerate(colors):
        if h >= height:
            (h1, color1), (h2, color2) = colors[i-1], colors[i]
            break
    result_color = color1 + (color2 - color1) * (height - h1) / (h2 - h1)
    return ''.join([hex_color(value) for value in result_color])

def get_land_color(height):
    return get_color(LAND_COLORS, height)

def get_water_color(height):
    return get_color(WATER_COLORS, height)