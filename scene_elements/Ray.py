from scene_elements.Point import Point
from helpers import vector_from_angle


class Ray:
    def __init__(self, origen, angle):
        self.origen = origen
        self.direccion = vector_from_angle(angle)
    def raySegmentIntersect(self, segmento):
        # calculate vectors
        v1 = self.origen - segmento.point1
        v2 = segmento.point2 - segmento.point1
        v3 = Point(-self.direccion.y, self.direccion.x)

        dot = v2.dot(v3)
        if (abs(dot) < 0.000001):
            return -1.0

        t1 = v2.cross(v1) / dot
        t2 = v1.dot(v3) / dot

        if (t1 >= 0.0 and (t2 >= 0.0 and t2 <= 1.0)):
            return t1

        return -1.0

    def getRayIntersectionPoint(self, dist):
        pt = Point()
        pt.x = self.origen.x + self.direccion.x * dist
        pt.y = self.origen.y + self.direccion.y * dist
        return pt

    def cast(self, segment):
        dist = self.raySegmentIntersect(segment)
        if dist == -1.0:
            return -1.0
        return self.getRayIntersectionPoint(dist)
