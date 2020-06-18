import math
from scene_elements.Point import Point
import numpy as np


def vectorFromAngle(angle, origen):
    return Point(1 * math.cos(angle), 1 * math.sin(angle))


def length(v1):
    # assumes v1 starts at (0,0)
    return math.sqrt(v1.x*v1.x + v1.y*v1.y)


def normalize(v1):
    # assumes v1 starts at (0,0)
    v1 = v1 / length(v1)
    return v1
def getLenght(v1,v2):
        dx=abs((v1.x-v2.x))
        dy=abs(v1.y -v2.y)
        return math.sqrt((dx**2)+(dy**2))
