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
import time
from helpers import getLenght
class threadPATH(Thread):
    mismopunto = 0
    def __init__(self,image_point,pixel_color):

        """Initialize the thread"""
        Thread.__init__(self)
        self.color=pixel_color
        self.image = image_point



    def run(self):
        rayosEfec=0
        for i in range(0, number_samples):
            # Iniciar rayos
            initial_ray = Ray(self.image, random.uniform(0, 360))
            # Iluminacion indirecta
            incoming_color = trace_path(initial_ray, 0)
            if not isinstance(incoming_color,type(np.array([0,0,0]))):
                continue
            self.color += incoming_color
            rayosEfec+=1
        canvas[int(self.image.x)][int(self.image.y)] = self.color // (len(light_sources) + rayosEfec)

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
    s=time.time()
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
                    intensidad = (1.2 - (light_distance / 500)) ** 2
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
            t = threadPATH(image_point,pixel_color)
            t.start()
    e=time.time()
    print(e-s)
def trace_path(rayo_actual, depth):
    # TODO FALTA IMPLEMENTAR ESTA FUNCION
    info_intersec=hitSomething(rayo_actual)
    punto = info_intersec[0]
    constanteIntensi=1
    if punto == -1.0:
        return -1
    pared=info_intersec[1]
    if pared.especularidad:
        constanteIntensi+=0.4
    distanciaPixWall=getLenght(rayo_actual.origen,punto)
    for source in light_sources:
        direccion=punto-source
        ray=Ray(source,0)
        ray.direccion=direccion
        info_intersec2=hitSomething(rayo_actual)
        punto=info_intersec2[0]
        if info_intersec2[1].horizontal:
            if  not (punto.y > source.y and punto.y > rayo_actual.origen.y) or not (punto.y < source.y and punto.y < rayo_actual.origen.y):
                return -1.0
        else:
            if  not (punto.x > source.x and punto.x > rayo_actual.origen.x) or not (punto.x < source.x and punto.x < rayo_actual.origen.x):
                return  -1.0
        if info_intersec2[0].x==punto.x and info_intersec2[0].y == punto.y:

            distanciaWallSource=getLenght(ray.origen,info_intersec2[0])
            distanciatotal=distanciaPixWall+distanciaWallSource
            intensidad =(constanteIntensi - (distanciatotal / 500)) ** 2
            colorWall2=np.array([color/100 for color in imagen[int(punto.y)][int(punto.x)][:3] ])
            refpix=imagen[rayo_actual.origen.y][rayo_actual.origen.x][:3]
            values = refpix * intensidad * colorWall2
            return values
        return -1.0



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
    img_file = Image.open("assets/Terraria.png")
    imagen = np.array(img_file)
    light_sources = [Point(75, 424),Point(283, 427),Point(473, 424),
                     Point(75,328),Point(282,329),Point(473,328),
                     Point(75, 253), Point(282, 253), Point(473, 253),
                     Point(29,473), Point(32,473),  Point(24,468)
                     ]
    # Color de la luz
    light_color = np.array([1, 1, 0.75])
    segments = [
        # Segment(Point(180, 135), Point(215, 135), True, False),
        # Segment(Point(285, 135), Point(320, 135), True, False),
        # Segment(Point(320, 135), Point(320, 280), False, False),
        # Segment(Point(320, 320), Point(320, 355), False, False),
        # Segment(Point(320, 355), Point(215, 355), True, False),
        # Segment(Point(180, 390), Point(180, 286), False, False),
        # Segment(Point(180, 286), Point(140, 286), True, False),
        # Segment(Point(320, 320), Point(360, 320), True, False),
        # Segment(Point(180, 250), Point(180, 135), False, False),

        #Primer Piso
        # PISO 1
        Segment(Point(62, 489), Point(487, 489), True, False),
        Segment(Point(62, 490), Point(487, 490), True, False),
        # PARED IZQUIERDA
        Segment(Point(62, 489), Point(62, 402), False, False),
        Segment(Point(62, 489), Point(62, 402), False, False),
        # PARTE 1 TECHO PRIMER PISO
        Segment(Point(62, 402), Point(111, 402), True, False),
        # PARTE 2 TECHO PRIMER PISO
        Segment(Point(150, 402), Point(486, 402), True, False),
        # PARED DERECHA
        Segment(Point(486, 402), Point(486, 489), False, False),
        #Segundo piso
        #Piso 1
        Segment(Point(64, 392), Point(112, 392), True, False),
        #Plataforma piso1
        Segment(Point(112, 392), Point(112, 403), False, False),
        #Plataforma de piso 1
        Segment(Point(149, 392), Point(149, 403), False, False),
        #Piso 2
        Segment(Point(149, 392),  Point(485, 392), True, False),
        #Pared piso 2 D
        Segment(Point(486, 393), Point(486 , 307), False, False),
        #Techo 1
        Segment(Point(486, 307), Point(149, 307), True, False),
        #Plataforma piso 2
        Segment(Point(149, 307), Point(149, 296), False, False),
        #Plataforma piso 2 I
        Segment(Point(112, 296), Point(112, 307), False, False),
        #Techo2
        Segment(Point(112, 307), Point(64, 307), True, False),
        #Pared piso 2 I
        Segment(Point(64, 307), Point(64, 392), False, False),
        #Tercer piso
        #Piso1
        Segment(Point(112, 296 ),Point(64, 296),True,True),
        #Pared I
        Segment(Point(64, 296), Point(64, 211), False, False),
        #Techo
        Segment(Point(64, 211), Point(486, 211), True, False),
        #Pared D
        Segment(Point(486, 211), Point(486, 296), False, False),
        #Suelo2
        Segment(Point(486, 296), Point(149, 296), True, False),
        #exterior
        #fogata
        Segment(Point(0, 489), Point(57, 489), False, False),
        # PARED IZQUIERDA AFUERA
        Segment(Point(57, 489), Point(57, 203), False, False),
        # TECHO ARRIBA
        Segment(Point(57, 203), Point(492, 203), True, False),
        # PARED DERECHA AFUERA
        Segment(Point(492, 203), Point(492, 486), False, False)


    ]
    path_trace_depth = 50
    number_samples = 5
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
