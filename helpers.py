import math
from scene_elements.Point import Point


def vector_from_angle(angle):
    """Retorna un vector a partir de un angulo

    :param angle: El angulo que se desea utilizar
    :return: El nuevo vector
    """
    return normalize(Point(1 * math.cos(angle), 1 * math.sin(angle)))


def get_vector_length(v1):
    """Obtiene el largo del vector

    :param v1: El vector
    :return: El largo enter (0, 0) y el punto del vector
    """
    # Se asume que el vector comienza en (0,0)
    return math.sqrt(v1.x * v1.x + v1.y * v1.y)


def normalize(v1):
    """Normaliza un vector

    :param v1: El vector que se desea normalizar
    :return: El vector normalizado
    """
    # Se asume que el vector comienza en (0,0)
    v1 = v1 / (get_vector_length(v1) + 0.1)  # Se suma 0.1 para evitar divisiones entre 0
    return v1


def get_length_between_points(punto1, punto2):
    """Obtiene el largo entre dos puntos

    :param punto1: El primer punto
    :param punto2: El segundo punto
    :return: El largo entre ambos puntos
    """
    dx = abs((int(punto1.x) - int(punto2.x)))
    dy = abs((int(punto1.y) - int(punto2.y)))
    return math.sqrt((dx ** 2) + (dy ** 2))


def ray_segment_intersect(origen, direccion, point1, point2):
    """Determina la interseccion entre un rayo y un segmento

    :param origen: El origen del rayo
    :param direccion: La direccion del rayo
    :param point1: El primer punto del rayo
    :param point2: El segundo punto del rayo
    :return: La distancia entre el origen del rayo y el segmento
    """
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
