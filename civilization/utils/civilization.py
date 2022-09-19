def decimal_hex(value):
    digits = '0123456789ABCDEF'
    r = digits[value//256]
    value = value%256
    g = digits[value//16]
    b = digits[value%16]
    return r+g+b