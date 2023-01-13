# -----------------------------------------------------------
# (c) 2023 Grant O
# -----------------------------------------------------------

from math import sqrt

def calculate_point_distance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# at 30 cm away it is 300px in height
size_to_dist_ratio = 10

def estimate_distance(height):
    return height / size_to_dist_ratio