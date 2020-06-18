import numpy as np
import pygame
import math
import random
import threading
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from scene_elements.Ray import Ray
from helpers import getLenght, length, ray_segment_intersect, normalize


def render():
    """Renderiza la imagen con iluminacion

    Args:
        canvas (Image): Imagen de la escena
        samples (int): Numero de samples por pixel
    """
    while True:
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
                        if distancia_interseccion != -1.0 and distancia_interseccion < light_distance:
                            free = False
                            break
                    # Verificar si no hay colision
                    if free:
                        # Calcular intensidad
                        intensidad = (1 - (light_distance / 500)) ** 2
                        # Obtener color del pixel
                        valores = (imagen[int(image_point.y)]
                                   [int(image_point.x)])[:3]
                        # Combinar color, fuente de luz y color de la luz
                        valores = valores * intensidad * light_color
                        # Agregar tofas las fuentes de luz
                        pixel_color += valores
                    # Promediar valor del pixel y asignar
                    canvas[int(image_point.x)][int(image_point.y)
                                               ] = pixel_color // len(light_sources)
            #         for o in range(samples):
            #             rayito=Ray(sources[0],math.radians(random.uniform(0,360)))
            #             np.add(canvas[i][u], pathTrace(rayito,0,2), out=canvas[i][u], casting="unsafe")
            #         canvas[i][u]= canvas[i][u]/samples
            #     print("x=", i)
            # print(canvas)


def pathTrace(ray, depth, maxDepth):
    Color2 = [random.uniform(0, 255), random.uniform(
        0, 255), random.uniform(0, 255)]
    # print(depth)
    if depth <= maxDepth:
        infoIntersec = hitSomething(ray)
        punto = infoIntersec[0]
        pared = infoIntersec[1]
        if punto == -1.0:
            return np.array([0, 0, 0])
        for source in light_sources:
            if source.x == punto.x and source.y == punto.y:
                return [imagen[source.x][source.y][:3]]
        rebote = anguloRebote(ray, punto, pared, depth)
        # pygame.draw.line(screen,Color,(ray.origen.x,ray.origen.y),(punto.x,punto.y),2)
        color_incoming = pathTrace(rebote, depth+1, maxDepth)
        distancia = getLenght(ray.origen, punto)
        intensity = (1 - (distancia / 500)) ** 2
        value = imagen[int(punto.x)-1][int(punto.y)-1][:3] * \
            intensity*color_incoming
        print(color_incoming)
        return value
    return np.array([0, 0, 0])


def randomPathTrace(depth, maxDepth):
    for i in range(1):
        ray = Ray(light_sources[0], math.radians(random.uniform(-360, 0)))
        color_incoming = pathTrace(ray, depth, maxDepth)


def anguloRebote(ray, punto, pared, depth):
    if pared.horizontal:
        if ray.origen.y > punto.y:
            # pared inferior
            angulo = math.radians(random.uniform(5, 175))
            #print("El rebote",depth, "debe ir abajo")
            return Ray(Point(punto.x, punto.y + 2), angulo)
        else:
            # pared superior
            angulo = math.radians(random.uniform(-175, -5))
            #print("El rebote" , depth , "debe ir arriba")
            return Ray(Point(punto.x, punto.y - 2), angulo)
    else:
        if ray.origen.x < punto.x:
            # pared derecha
            angulo = math.radians(random.uniform(-270, -90))
            #print("El rebote" , depth , "debe ir a la izquierda")
            return Ray(Point(punto.x - 2, punto.y), angulo)
        else:
            # pared izquierda
            angulo = math.radians(random.uniform(-85, 85))
            #print("El rebote" ,depth , "debe ir a la derecha")
            return Ray(Point(punto.x + 2, punto.y), angulo)


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


def getFrame():
    pixels = np.roll(canvas, (1, 2), (0, 1))
    return pixels


# MAIN PROGRAM
if __name__ == "__main__":
    # Color = [0, 0, 0]
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

    img_file = Image.open("fondo.png")
    imagen = np.array(img_file)
    light_sources = [Point(195, 200), Point(294, 200)]
    # Color de la luz
    light_color = np.array([1, 1, 0.75])
    segments = [
        Segment(Point(0, 0), Point(500, 0), True, False),
        Segment(Point(0, 0), Point(0, 500), False, False),
        Segment(Point(0, 500), Point(500, 500), True, False),
        Segment(Point(500, 500), Point(500, 0), False, False),
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

    # Setup de los threads
    t = threading.Thread(target=render)
    t.setDaemon(True)  # Alternatively, you can use "t.daemon = True"
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
