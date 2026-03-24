import constantes
import pygame
from personaje import Personaje

from constantes import ANCHO_VENTANA, ALTO_VENTANA

pacman = Personaje(350, 350)

pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

pygame.display.set_caption('Pacman')

#definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

# Controlar los frames
reloj = pygame.time.Clock()

run = True

while run:

    #Frames limitados
    reloj.tick(constantes.FPS)

    ventana.fill(constantes.COLOR_FONDO)

    #Calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = 5

    if mover_izquierda == True:
        delta_x = -5

    if mover_abajo == True:
        delta_y = -5

    if mover_arriba == True:
        delta_y = 5

    pacman.movimiento(delta_x, delta_y)

    print(f"{delta_x},s{delta_y}")

    pacman.dibujar(ventana)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_abajo = True
            if event.key == pygame.K_s:
                mover_arriba = True

    pygame.display.update()
