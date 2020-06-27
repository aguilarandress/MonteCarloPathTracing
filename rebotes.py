import math
import random
import numpy as np
from scene_elements.Ray import Ray
from scene_elements.Point import Point
from scene_elements.Segment import Segment


def crear_rayo_aleatorio(ray, punto, pared):
    """Crea un rayo aleatorio a partir del rabote

    :param ray: El rayo actual
    :param punto: El punto de interseccion entre el rayo y la pared
    :param pared: La pared de interseccion
    :return: Un rayo con el origen en el punto de rebote
    """
    # Verificar especularidad
    if pared.especularidad:
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


# TODO: Verificar que sucede si ambas rectas son perpendiculares
def crear_rayo_especular(ray, punto, pared):
    """Crea un rayo especular

    :param ray: El rayo saliente
    :param punto: El punto de interseccion del rayo
    :param pared: La pared de interseccion
    :return: El rayo especular
    """
    # Obtener angulo
    angulo = np.rad2deg(get_angle_between(Segment(ray.origen, punto,False,False), pared))
    if pared.horizontal:
        # Por arriba
        if ray.origen.y > punto.y:
            # Por la derecha
            if ray.origen.x > punto.x:
                return Ray(Point(punto.x, punto.y + 2), math.radians(2*(90-angulo)+angulo))
            else:
                return Ray(Point(punto.x, punto.y + 2), math.radians(-angulo))
            # Por la derecha
        else:
            # Por abajo
            if ray.origen.x > punto.x:

                return Ray(Point(punto.x, punto.y - 2), math.radians(180-angulo))
            else:

                return Ray(Point(punto.x, punto.y - 2), math.radians(-(180+(angulo - 180))))
    else:
        # Vertical y por la derecha
        if ray.origen.x > punto.x:
            # Por arriba
            if ray.origen.y > punto.y:
                return Ray(Point(punto.x + 2, punto.y), math.radians(-(90-angulo)))
            # Por abajo
            else:
                print(angulo)
                return Ray(Point(punto.x + 2, punto.y), math.radians(-(90-angulo)))
        else:
            # Por abajo
            if ray.origen.y > punto.y:
                return Ray(Point(punto.x - 2, punto.y), math.radians(angulo+90))
            # Por arriba
            else:
                return Ray(Point(punto.x - 2, punto.y), math.radians(angulo+90))


def get_angle_between(segmento_rayo, segmento):
    """Obtiene el angulo entre dos rectas

    :param segmento_rayo: El segmento que creado a partir del rayo
    :param segmento: El segmento de interseccion
    :return: El angulo entre ambas rectas
    """
    # Determinar verticalidad de los segmentos
    verticalidad_rayo = segmento_rayo.point1.x - segmento_rayo.point2.x == 0.0
    verticalidad_segmento = segmento.point1.x - segmento.point2.x == 0
    # Ambas lineas son verticales
    if verticalidad_rayo and verticalidad_segmento:
        return 0.0
    # Verificar si alguna de las dos es vertical
    if verticalidad_segmento or verticalidad_rayo:
        segmento_no_vertical = segmento_rayo if verticalidad_segmento else segmento
        return abs((90.0 * np.pi / 180.0) - np.arctan(segmento_no_vertical.determinar_pendiente()))
    pendiente_rayo = segmento_rayo.determinar_pendiente()
    pendiente_segmento = segmento.determinar_pendiente()
    return np.arctan((pendiente_rayo - pendiente_segmento) / (1 + pendiente_rayo * pendiente_segmento))