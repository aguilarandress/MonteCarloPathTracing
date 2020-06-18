from threading import Thread
from scene_elements import Point
from helpers import *
import pygame
class MyThread(Thread):
    """
    A threading example
    """

    def __init__(self,rr,cc,imagen,canvas):
        """Initialize the thread"""
        Thread.__init__(self)
        self.rr = rr
        self.cc = cc
        self.imagen=imagen
        self.canvas=canvas

    def run(self):
        values = self.imagen[self.rr][self.cc][:3]
        length = getLenght(self.sources[0], Point(rr, cc))
        intensity = (1 - (length / 500)) ** 2
        values = values * intensity * light
        self.canvas[self.rr][self.cc] = values
        surface = pygame.surfarray.make_surface(canvas)
        screen.blit(surface, (border, border))


if __name__ == "__main__":
    create_threads()