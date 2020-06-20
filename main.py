import numpy as np
import pygame
import math
import random
import threading
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from scene_elements.Ray import Ray
from helpers import length, ray_segment_intersect, normalize
from threading import Thread
class threadPATH(Thread):
    def __init__(self,image_point):
        """Initialize the thread"""
        Thread.__init__(self)
        self.image = image_point



    def run(self):
        for i in range(0, number_samples):
            # Iniciar rayos
            initial_ray = Ray(self.image, random.uniform(0, 360))
            # Iluminacion indirecta
            incoming_color = trace_path(initial_ray, 0)
            if incoming_color == -1.0:
                pass
            # pixel_color += incoming_color
        # canvas[int(image_point.x)][int(image_point.y)] = pixel_color // (len(light_sources) + number_samples)

def hitSomething(ray):
    closest = -1.0
    hittedWall = None
    record = 1000000000
    for wall in segments:
        point = ray.cast(wall)
        if point != -1:
            dist = ray.raySegmentIntersect(wall)
            if dist < record:
                record = dist
                closest = point
                hittedWall = wall
    return [closest, hittedWall]


def render():
    """Renderiza la imagen con iluminacion

    Args:
        canvas (Image): Imagen de la escena
        samples (int): Numero de samples por pixel
    """
    for i in range(len(canvas)):
        for j in range(len(canvas)):
            # Obtener punto en la imagen
            image_point = Point(i, j)
            pixel_color = 0
            for light_source in light_sources:
                # Calcular direccion a la
                direccion = light_source - image_point
                light_distance = length(direccion)
                # Verificar con interseccion en la pared
                free = True
                for wall in segments:
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
                    intensidad = (1.7 - (light_distance / 500)) ** 2
                    # Obtener color del pixel
                    valores = (imagen[int(image_point.y)]
                               [int(image_point.x)])[:3]
                    # Combinar color, fuente de luz y color de la luz
                    valores = valores * intensidad * light_color
                    # Agregar todas las fuentes de luz
                    pixel_color += valores
                # Promedia pixel y asignar valor
                canvas[int(image_point.x)][int(image_point.y)
                                           ] = pixel_color // len(light_sources)
            #TODO PATH TRACING O ILUMINACION INDIRECTA
            t = threadPATH(image_point)
            t.start()


def trace_path(rayo_actual, depth):
    #atan2(y2−y1,x2−x1)
    # TODO FALTA IMPLEMENTAR ESTA FUNCION
    info_intersec=hitSomething(rayo_actual)
    punto = info_intersec[0]
    pared = info_intersec[1]
    if punto == -1.0:
        return -1
    for source in light_sources:
        direccion=punto-source
        light_distance = length(direccion)
        ray=Ray(source,0)
        ray.direccion=direccion
        info_intersec2=hitSomething(rayo_actual)
        pygame.draw.circle(screen, [255, 100, 100], (int(info_intersec2[0].x), int(info_intersec2[0].y)),10)
        pygame.draw.circle(screen, [100, 255, 100], (int(punto.x), int(punto.y)), 3)





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
    img_file = Image.open("assets/fondo.png")
    imagen = np.array(img_file)
    light_sources = [Point(195, 200), Point(294, 200)]
    # Color de la luz
    light_color = np.array([1, 1, 0.75])
    segments = [
        # Segment(Point(0, 0), Point(500, 0), True, False),
        # Segment(Point(0, 0), Point(0, 500), False, False),
        # Segment(Point(0, 500), Point(500, 500), True, False),
        # Segment(Point(500, 500), Point(500, 0), False, False),
        Segment(Point(180, 135), Point(215, 135), True, False),
        Segment(Point(285, 135), Point(320, 135), True, False),
        Segment(Point(320, 135), Point(320, 280), False, False),
        Segment(Point(320, 320), Point(320, 355), False, False),
        Segment(Point(320, 355), Point(215, 355), True, False),
        Segment(Point(180, 390), Point(180, 286), False, False),
        Segment(Point(180, 286), Point(140, 286), True, False),
        Segment(Point(320, 320), Point(360, 320), True, False),
        Segment(Point(180, 250), Point(180, 135), False, False),
    ]
    path_trace_depth = 50
    number_samples = 3
    # Setup de los threads
    t = threading.Thread(target=render)
    t.setDaemon(True)
    t.start()
    # Main loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Clear screen to white before drawing
        screen.fill((255, 255, 255))
        npimage = getFrame()
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))
        pygame.display.flip()
        clock.tick(60)
