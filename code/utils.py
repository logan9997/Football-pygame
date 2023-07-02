import math

def distance_two_points(x1, x2, y1, y2):
    return math.sqrt(
        math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)
    )
