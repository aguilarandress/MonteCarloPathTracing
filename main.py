import time
import pygame
import random
import threading
import numpy as np
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from scene_elements.Ray import Ray
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
                incoming_color = trace_path(initial_ray, 0)
                # Verificar si se obtiene un color
                if not isinstance(incoming_color, type(np.array([0, 0, 0]))):
                    continue
                pixel_color += incoming_color
                rayos_efectivos += 1
            # Promediar color final
            canvas[int(image_point.x)][int(image_point.y)] = pixel_color // (len(light_sources) + rayos_efectivos)
    e = time.time()
    print(e - s)


def trace_path(rayo_actual, depth):
    """Se encarga de realizar el trazado de rayos para la iluminacion indirecta

    :param rayo_actual: El rayo actual que se esta trazando
    :param depth:
    :return: El color calculado mediante el path tracing
    """
    # Check intersection point
    info_interseccion = check_wall_intersection(rayo_actual)
    punto = info_interseccion[0]
    if punto == -1.0:
        return -1
    # Obtener distancia entre ambos puntos
    distancia_interseccion = get_length_between_points(rayo_actual.origen, punto)
    for source in light_sources:
        # Crear rayo desde la fuente de luz hacia la interseccion
        direccion = punto - source
        ray = Ray(source,0)
        ray.direccion = normalize(direccion)
        # Verificar interseccion
        info_light_interseccion = check_wall_intersection(ray)
        punto2 = info_light_interseccion[0]
        if punto2 == -1.0:
            continue
        # Verificar que ambas intersecciones coincidan
        if int(punto2.x) == int(punto.x) and int(punto2.y) == int(punto.y):
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
            intensidad = (1 - (distancia_total / 500)) ** 2
            # Calcular color nuevo
            color_interseccion = np.array([color/100 for color in imagen[int(punto.y)][int(punto.x)][:3] ])
            color_origen = imagen[rayo_actual.origen.y][rayo_actual.origen.x][:3]
            values = color_origen * intensidad * color_interseccion
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
    # window = pygame.display.set_mode((600, 600))
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
    light_sources = [
        Point(195, 200), Point( 294, 200)]
        #             Point(75, 424),Point(283, 427),Point(473, 424),
        #              Point(75,328),Point(282,329),Point(473,328),
        #
        #              Point(29,473), Point(32,473),  Point(24,468)]

    # Color de la luz
    light_color = np.array([1, 1, 0.75])
    segments = [
        Segment(Point(180, 135), Point(215, 135), True, False),
        Segment(Point(285, 135), Point(320, 135), True, False),
        Segment(Point(320, 135), Point(320, 280), False, False),
        Segment(Point(320, 320), Point(320, 355), False, False),
        Segment(Point(320, 355), Point(215, 355), True, False),
        Segment(Point(180, 390), Point(180, 286), False, False),
        Segment(Point(180, 286), Point(140, 286), True, False),
        Segment(Point(320, 320), Point(360, 320), True, False),
        Segment(Point(180, 250), Point(180, 135), False, False),

        #Primer Piso
        # # PISO 1
        # Segment(Point(62, 489), Point(487, 489), True, False),
        # # PARED IZQUIERDA
        # Segment(Point(62, 489), Point(62, 402), False, False),
        # # PARTE 1 TECHO PRIMER PISO
        # Segment(Point(62, 402), Point(111, 402), True, False),
        # # PARTE 2 TECHO PRIMER PISO
        # Segment(Point(150, 402), Point(486, 402), True, False),
        # # PARED DERECHA
        # Segment(Point(486, 402), Point(486, 489), False, False),
        # #Segundo piso
        # #Piso 1
        # Segment(Point(64, 392), Point(112, 392), True, False),
        # #Plataforma piso1
        # Segment(Point(112, 392), Point(112, 403), False, False),
        # #Plataforma de piso 1
        # Segment(Point(149, 392), Point(149, 403), False, False),
        # #Piso 2
        # Segment(Point(149, 392),  Point(485, 392), True, False),
        # #Pared piso 2 D
        # Segment(Point(486, 393), Point(486 , 307), False, False),
        # #Techo 1
        # Segment(Point(486, 307), Point(149, 307), True, False),
        # #Plataforma piso 2
        # Segment(Point(149, 307), Point(149, 296), False, False),
        # #Plataforma piso 2 I
        # Segment(Point(112, 296), Point(112, 307), False, False),
        # #Techo2
        # Segment(Point(112, 307), Point(64, 307), True, False),
        # #Pared piso 2 I
        # Segment(Point(64, 307), Point(64, 392), False, False),
        # #Tercer piso
        # #Piso1
        # Segment(Point(112, 296 ),Point(64, 296),True,False),
        # #Pared I
        # Segment(Point(64, 296), Point(64, 211), False, False),
        # #Techo
        # Segment(Point(64, 211), Point(486, 211), True, False),
        # #Pared D
        # Segment(Point(486, 211), Point(486, 296), False, False),
        # #Suelo2
        # Segment(Point(486, 296), Point(149, 296), True, False),
        # #exterior
        # #fogata
        # Segment(Point(0, 489), Point(57, 489), False, False),
        # # PARED IZQUIERDA AFUERA
        # Segment(Point(57, 489), Point(57, 203), False, False),
        # # TECHO ARRIBA
        # Segment(Point(57, 203), Point(492, 203), True, False),
        # # PARED DERECHA AFUERA
        # Segment(Point(492, 203), Point(492, 486), False, False)
    ]
    path_trace_depth = 50
    number_samples = 10
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
        # screen.fill((0, 0, 0))
        npimage = getFrame()
        surface = pygame.surfarray.make_surface(npimage)
        # screen.blit(surface, (border, border))
        pygame.display.flip()
        clock.tick(60)
