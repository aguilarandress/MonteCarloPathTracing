import numpy as np
import pygame
import math
import random
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from scene_elements.Ray import Ray
from helpers import vectorFromAngle


def main():
    """Funcion principal de la aplicacion
    """
    # Segmentos y fuentes
    segments = [
        Segment(Point(0, 0), Point(500, 0), False),
        Segment(Point(0, 0), Point(0, 500), False),
        Segment(Point(0, 500), Point(500, 500), False),
        Segment(Point(500, 500), Point(500, 0), False),
        Segment(Point(180, 135), Point(215, 135), False),
        Segment(Point(285, 135), Point(320, 135), False),
        Segment(Point(320, 135), Point(320, 280), False),
        Segment(Point(320, 320), Point(320, 355), False),
        Segment(Point(320, 355), Point(215, 355), False),
        Segment(Point(180, 390), Point(180, 286), False),
        Segment(Point(180, 286), Point(140, 286), False),
        Segment(Point(320, 320), Point(360, 320), False),
        Segment(Point(180, 250), Point(180, 135), False),
    ]
    sources = [Point(250, 250)]
    # Crear ventana
    HEIGHT, WIDTH = 500, 500
    border = 50
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    screen = pygame.display.set_mode(
        (WIDTH + (2 * border), HEIGHT + (2 * border)))
    pygame.display.set_caption("Path Tracer")
    clock = pygame.time.Clock()
    # Cargar imagen
    img_file = Image.open("assets/fondoW.png")
    img_ref = np.array(img_file)
    # Desplegar imagen
    surface = pygame.surfarray.make_surface(img_ref)
    screen.blit(surface, (border, border))
    # Crear segmentos
    Color = [0, 0, 0]
    for segment in segments:
        pygame.draw.line(window, Color, (segment.point1.x,
                                         segment.point1.y), (segment.point2.x, segment.point2.y), 4)
    pygame.draw.circle(window, Color, (sources[0].x, sources[0].y), 2, 1)
    # Crear el rayo
    for i in range(-360, 1, 1):
        ray = Ray(sources[0], math.radians(i))
        closest = None
        record = 100000000000000000
        for wall in segments:
            point = ray.cast(wall)
            if point != -1.0:
                dist = ray.raySegmentIntersect(wall)
                if dist < record:
                    record = dist
                    closest = point
        if isinstance(closest, Point):
            pygame.draw.line(window, Color, (sources[0].x,
                                             sources[0].y), (closest.x, closest.y), 1)
    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


if __name__ == "__main__":
    main()
