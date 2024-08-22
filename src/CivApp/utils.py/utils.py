def map_value(value, min1, max1, min2, max2):
    value = max(min(value, max1), min1)
    span1 = max1 - min1
    span2 = max2 - min2

    value_scaled = float(value - min1) / float(span1)

    return min2 + (value_scaled * span2)