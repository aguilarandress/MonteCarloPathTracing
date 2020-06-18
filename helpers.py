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
def _bresenhamline_nslope(slope):

    scale = np.amax(np.abs(slope), axis=1).reshape(-1, 1)
    zeroslope = (scale == 0).all(1)
    scale[zeroslope] = np.ones(1)
    normalizedslope = np.array(slope, dtype=np.double) / scale
    normalizedslope[zeroslope] = np.zeros(slope[0].shape)
    return normalizedslope

def _bresenhamlines(start, end, max_iter):

    if max_iter == -1:
        max_iter = np.amax(np.amax(np.abs(end - start), axis=1))
    npts, dim = start.shape
    nslope = _bresenhamline_nslope(end - start)

    # steps to iterate on
    stepseq = np.arange(1, max_iter + 1)
    stepmat = np.tile(stepseq, (dim, 1)).T

    # some hacks for broadcasting properly
    bline = start[:, np.newaxis, :] + nslope[:, np.newaxis, :] * stepmat

    # Approximate to nearest int
    return np.array(np.rint(bline), dtype=start.dtype)

def bresenhamline(start, end, max_iter=5):

    # Return the points as a single array
    return _bresenhamlines(start, end, max_iter).reshape(-1, start.shape[-1])