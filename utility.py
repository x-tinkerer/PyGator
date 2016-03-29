
def arr2int(bytes, size):
    result = 0
    for i in range(0, size):
        result |= bytes[i] << (8 * i)
    return result