from scene_elements.Point import Point
from helpers import vector_from_angle


class Ray:
    """Clase para representar un rayo de luz en la escena
    """
    def __init__(self, origen, angle):
        self.origen = origen
        self.direccion = vector_from_angle(angle)


    def ray_segment_intersect(self, segmento):
        """Calcula la distancia entre el punto de interseccion y el origen del rayo

        :param segmento: El segmento que se desea verificar
        :return: La distancia entre ambos puntos
        """
        # calculate vectors
        v1 = self.origen - segmento.point1
        v2 = segmento.point2 - segmento.point1
        v3 = Point(-self.direccion.y, self.direccion.x)
        dot = v2.dot(v3)
        if abs(dot) < 0.000001:
            return -1.0
        t1 = v2.cross(v1) / dot
        t2 = v1.dot(v3) / dot
        if t1 >= 0.0 and (t2 >= 0.0 and t2 <= 1.0):
            return t1
        return -1.0


    def get_ray_intersection_point(self, dist):
        """Calcular el punto de interseccion entre el rayo y el segmento

        :param dist: La distancia entre ambos puntos
        :return: El punto de interseccion entre el rayo y el segmento
        """
        pt = Point()
        pt.x = self.origen.x + self.direccion.x * dist
        pt.y = self.origen.y + self.direccion.y * dist
        return pt


    def cast(self, segment):
        """Genera un rayo hacia un segmento

        :param segment: El segmento que se desea verificar
        :return: El punto de interseccion entre el rayo y el segmento
        """
        dist = self.ray_segment_intersect(segment)
        if dist == -1.0:
            return -1.0
        return self.get_ray_intersection_point(dist)
