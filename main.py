import constantes
import pygame
from personaje import Personaje

from constantes import ANCHO_VENTANA, ALTO_VENTANA

pacman = Personaje(350, 350)

pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

pygame.display.set_caption('Pacman')

#Fuentes
font_inicio = pygame.font.SysFont('Comic Sans MS', 30)
font_titulo = pygame.font.SysFont('Comic Sans MS', 60)

boton_jugar = pygame.Rect(constantes.ANCHO_VENTANA / 2 + 100,
                          constantes.ALTO_VENTANA / 2 - 50, 200, 50)
boton_salir = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100,
                          constantes.ALTO_VENTANA / 2 + 50, 200, 50)
texto_boton_jugar = font_inicio.render('Jugar', True, (255, 255, 255))
texto_boton_salir = font_inicio.render('Salir', True, (255, 255, 255))
rect_texto_jugar = texto_boton_jugar.get_rect(center=boton_jugar.center)
rect_texto_salir = texto_boton_salir.get_rect(center=boton_salir.center)

ventana.blit(texto_boton_jugar, rect_texto_jugar)
ventana.blit(texto_boton_salir, rect_texto_salir)

#definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

# Controlar los frames
reloj = pygame.time.Clock()

estado = "menu"

run = True

while run:

    if estado == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    estado = "juego"
                if boton_salir.collidepoint(event.pos):
                    run = False

        ventana.fill(constantes.MORADO)

        pygame.draw.rect(ventana, (0, 0, 0), boton_jugar)
        pygame.draw.rect(ventana, (0, 0, 0), boton_salir)

        # Dibujar texto
        ventana.blit(texto_boton_jugar, (boton_jugar.x + 20, boton_jugar.y + 60))
        ventana.blit(texto_boton_salir, (boton_salir.x + 20, boton_salir.y + 90))

    elif estado == "juego":
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
            delta_y = 5

        if mover_arriba == True:
            delta_y = -5

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
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False

    pygame.display.update()

