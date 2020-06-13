import numpy as np
import pygame
from PIL import Image
from scene_elements.Point import Point
from scene_elements.Segment import Segment


def main():
    """Funcion principal de la aplicacion
    """
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
    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


if __name__ == "__main__":
    main()
