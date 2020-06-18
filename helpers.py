import math
from scene_elements.Point import Point


def vectorFromAngle(angle, origen):
    return Point(1 * math.cos(angle), 1 * math.sin(angle))


def length(v1):
    # assumes v1 starts at (0,0)
    return math.sqrt(v1.x*v1.x + v1.y*v1.y)


def normalize(v1):
    # assumes v1 starts at (0,0)
    v1 = v1 / length(v1)
    return v1

def getLenght(punto1,punto2):
    dx = abs((punto1.x - punto2.x))
    dy = abs((punto1.y - punto2.y))
    return math.sqrt((dx**2)+(dy**2))

def ray_segment_intersect(origen, direccion, point1, point2):
    # Calcular vectores
    v1 = origen - point1
    v2 = point2 - point1
    v3 = Point(-direccion.y, direccion.x)

    dot = v2.dot(v3)
    if (abs(dot) < 0.000001):
        return -1.0
    t1 = v2.cross(v1) / dot
    t2 = v1.dot(v3) / dot
    if (t1 >= 0.0 and (t2 >= 0.0 and t2 <= 1.0)):
        return t1
    return -1.0

