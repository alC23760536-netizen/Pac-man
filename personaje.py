import pygame
import constantes
from constantes import TAMAÑO_PERSONAJE, COLOR_PERSONAJE


class Personaje:
    def __init__(self, x, y, radio=TAMAÑO_PERSONAJE, color=COLOR_PERSONAJE):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color

    def dibujar(self, interfaz):
        pygame.draw.circle(interfaz, self.color, (self.x, self.y), self.radio)

    def movimiento(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y