import math
import random
from scene_elements.Ray import Ray
from scene_elements.Point import Point


def crear_rayo_aleatorio(ray, punto, pared):
    """Crea un rayo aleatorio a partir del rabote

    :param ray: El rayo actual
    :param punto: El punto de interseccion entre el rayo y la pared
    :param pared: La pared de interseccion
    :return: Un rayo con el origen en el punto de rebote
    """
    # Verificar especularidad
    if pared.especularidad:
        # TODO Implementar especularidad aqui
        return crear_rayo_especular(ray, punto, pared)
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


def crear_rayo_especular(ray, punto, pared):
    # TODO Implementar esta funcion
    pass