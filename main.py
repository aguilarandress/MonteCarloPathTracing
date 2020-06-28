import time
import pygame
import random
import threading
import numpy as np
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from scene_elements.Ray import Ray
from rebotes import crear_rayo_especular
from helpers import get_vector_length, get_length_between_points, ray_segment_intersect, normalize


def render():
    """Renderiza la imagen con iluminacion global

    :return:
    """
    s = time.time()
    for i in range(len(canvas)):
        for j in range(len(canvas)):
            # Obtener punto en la imagen
            image_point = Point(i, j)
            pixel_color = 0
            for light_source in light_sources:
                # Calcular direccion a la
                direccion = light_source - image_point
                light_distance = get_vector_length(direccion)
                # Verificar con interseccion en la pared
                free = True
                for wall in segments:
                    if wall.transparencia:
                        continue
                    # Revisar interseccion
                    distancia_interseccion = ray_segment_intersect(
                        image_point, normalize(direccion), wall.point1, wall.point2)
                    # Verificar colision
                    if distancia_interseccion != -1.0 and distancia_interseccion < light_distance:
                        free = False
                        break
                # Verificar si no hay colision
                if free:
                    # Calcular intensidad
                    intensidad = (1.2 - (light_distance / 500)) ** 2
                    # Obtener color del pixel
                    valores = (imagen[int(image_point.y)]
                               [int(image_point.x)])[:3]
                    # Combinar color, fuente de luz y color de la luz
                    valores = valores * intensidad * light_color

                    # Agregar todas las fuentes de luz
                    pixel_color += valores
                # Promedia pixel y asignar valor
                canvas[int(image_point.x)][int(image_point.y)] = pixel_color // len(light_sources)
            # Realizar Monte Carlo Path tracing
            rayos_efectivos = 0
            for samples in range(0, number_samples):
                # Iniciar rayos
                initial_ray = Ray(image_point, random.uniform(0, 360))
                # Iluminacion indirecta
                incoming_color = trace_path(initial_ray)
                # Verificar si se obtiene un color
                if not isinstance(incoming_color, type(np.array([0, 0, 0]))):
                    continue
                pixel_color += incoming_color
                rayos_efectivos += 1
            # Promediar color final
            canvas[int(image_point.x)][int(image_point.y)] = pixel_color // (len(light_sources) + rayos_efectivos)
    e = time.time()
    print(e - s)



def trace_path(rayo_actual):
    """Se encarga de realizar el trazado de rayos para la iluminacion indirecta

    :param rayo_actual: El rayo actual que se esta trazando
    :return: El color calculado mediante el path tracing
    """
    # Check intersection point
    info_interseccion = check_wall_intersection(rayo_actual)
    punto = info_interseccion[0]
    pared=info_interseccion[1]
    if punto == -1.0:
        return -1.0
    # Obtener distancia entre ambos puntos
    intensidad_inicial = 1
    distancia_interseccion = get_length_between_points(rayo_actual.origen, punto)
    for source in light_sources:
        punto_interseccion = punto
        # Verificar especularidad
        if pared.especularidad:
            # TODO: Verificar que sucede si el rayo es de 90 grados
            rayo_especular = crear_rayo_especular(rayo_actual, punto, pared)
            rayo_actual = rayo_especular
            # Verificar interseccion del rayo especular
            info_especular = check_wall_intersection(rayo_especular)
            punto_interseccion_especular = info_especular[0]
            if punto_interseccion_especular == -1:
                return -1.0
            distancia_interseccion = distancia_interseccion + get_length_between_points(punto, punto_interseccion_especular)
            punto_interseccion = punto_interseccion_especular
            intensidad_inicial = 1.3

        # Crear rayo desde la fuente de luz hacia la interseccion
        direccion = punto_interseccion - source
        ray = Ray(source,0)
        ray.direccion = normalize(direccion)
        # Verificar interseccion
        info_light_interseccion = check_wall_intersection(ray)
        punto2 = info_light_interseccion[0]
        if punto2 == -1.0:
            continue
        # Verificar que ambas intersecciones coincidan
        if int(punto2.x) == int(punto_interseccion.x) and int(punto2.y) == int(punto_interseccion.y):
            # Verificar que la fuente de luz y el pixel se encuentren en el mismo lado del segmento
            if info_light_interseccion[1].horizontal:
                if not ((punto2.y > source.y and punto2.y > rayo_actual.origen.y) or (
                        punto2.y < source.y and punto2.y < rayo_actual.origen.y)):
                    return -1.0
            else:
                if not ((punto2.x > source.x and punto2.x > rayo_actual.origen.x) or (
                        punto2.x < source.x and punto2.x < rayo_actual.origen.x)):
                    return -1.0
            # Calcular distancia total
            distancia_light_segment = get_length_between_points(ray.origen, info_light_interseccion[0])
            distancia_total = distancia_interseccion + distancia_light_segment
            intensidad = (intensidad_inicial - (distancia_total / 500)) ** 2
            # Calcular color nuevo
            color_interseccion = np.array([color / 190 for color in imagen[int(punto.y) - 1][int(punto.x) - 1][:3]])
            color_origen = imagen[int(rayo_actual.origen.y)][int(rayo_actual.origen.x)][:3]
            values = color_origen * intensidad * (color_interseccion * light_color)
            return values
    return  -1.0


def check_wall_intersection(ray):
    """Verifica si el rayo interseca con un segmento

    :param ray: El rayo que se generando
    :return: La interseccion con la pared
    """
    closest = -1.0
    hitted_wall = None
    record = 1000000000
    # Check all segments
    for wall in segments:
        # Cast a new ray
        point = ray.cast(wall)
        if point != -1:
            dist = ray.ray_segment_intersect(wall)
            if dist < record:
                record = dist
                closest = point
                hitted_wall = wall
    return [closest, hitted_wall]


def getFrame():
    pixels = np.roll(canvas, (1, 2), (0, 1))
    return pixels


# MAIN PROGRAM
if __name__ == "__main__":
    # Crear ventana
    HEIGHT, WIDTH = 550, 550
    border = 50
    pygame.init()
    screen = pygame.display.set_mode(
        (WIDTH + (2 * border), HEIGHT + (2 * border)))
    # Segmentos y fuentes
    pygame.display.set_caption("Path Tracer")
    done = False
    clock = pygame.time.Clock()
    # Init random
    random.seed()
    blank = Image.new("RGB", (500, 500), (0, 0, 0))
    canvas = np.array(blank)
    # Load image file
    img_file = Image.open("assets/roomBleed.png")
    imagen = np.array(img_file)
    light_sources = [Point(195, 200), Point(294, 200)]
    # Color de la luz
    light_color = np.array([1, 1, 0.75])
    segments = [
        Segment(Point(180, 135), Point(215, 135), True, False),
        Segment(Point(285, 135), Point(320, 135), True, False),
        Segment(Point(320, 135), Point(320, 280), False, False),
        Segment(Point(320, 320), Point(320, 355), False, False),
        Segment(Point(320, 355), Point(215, 355), True, False),
        Segment(Point(180, 390), Point(180, 286), False, False),
        Segment(Point(180, 286), Point(140, 286), True, False,True),
        Segment(Point(320, 320), Point(360, 320), True, False),
        Segment(Point(180, 250), Point(180, 135), False, False),
    ]
    number_samples = 30
    # Setup de los threads
    t = threading.Thread(target=render)
    t.setDaemon(True)
    t.start()
    # Main loop
    for segment in segments:
        pygame.draw.line(screen,[255,255,255],(segment.point1.x,segment.point1.y),(segment.point2.x,segment.point2.y),2)
    for lig in light_sources:
        pygame.draw.circle(screen,[50,0,20],(lig.x,lig.y),5)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Clear screen to white before drawing
        screen.fill((0, 0, 0))
        npimage = getFrame()
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))
        pygame.display.flip()
        clock.tick(60)
