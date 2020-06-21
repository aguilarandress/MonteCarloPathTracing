import math
from scene_elements.Point import Point


def vector_from_angle(angle, origen):
    return Point(1 * math.cos(angle), 1 * math.sin(angle))


def length(v1):
    # assumes v1 starts at (0,0)
    return math.sqrt(v1.x * v1.x + v1.y * v1.y)


def normalize(v1):
    # assumes v1 starts at (0,0)
    v1 = v1 / (length(v1) + 0.1)  # Se suma 0.1 para evitar divisiones entre 0
    return v1


def getLenght(punto1, punto2):
    dx = abs((int(punto1.x) - int(punto2.x)))
    dy = abs((int(punto1.y) - int(punto2.y)))
    return math.sqrt((dx ** 2) + (dy ** 2))


def angulo_rebote(ray, punto, pared):
    """Genera un anglo aleatorio en el segmento

    Args:
        ray (Ray): El rayo de entrada
        punto (Point): Punto de interseccion en el segmento
        pared (Segment): Segmento de interseccion

    Returns:
        Ray: Un nuevo rayo con origen y angulo aleatorio
    """
    if pared.horizontal:
        if ray.origen.y > punto.y:
            # pared inferior
            angulo = math.radians(random.uniform(5, 175))
            return Ray(Point(punto.x, punto.y + 2), angulo)
        else:
            # pared superior
            angulo = math.radians(random.uniform(-175, -5))
            return Ray(Point(punto.x, punto.y - 2), angulo)
    else:
        if ray.origen.x < punto.x:
            # pared derecha
            angulo = math.radians(random.uniform(-270, -90))
            return Ray(Point(punto.x - 2, punto.y), angulo)
        else:
            # pared izquierda
            angulo = math.radians(random.uniform(-85, 85))
            return Ray(Point(punto.x + 2, punto.y), angulo)


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
