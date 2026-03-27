import constantes
import pygame
from personaje import Personaje

from constantes import ANCHO_VENTANA, ALTO_VENTANA

pacman = Personaje(350, 350)

pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Pacman')

# Fuentes
font_inicio = pygame.font.SysFont('Comic Sans MS', 30)
font_titulo = pygame.font.SysFont('Comic Sans MS', 60)
font_input = pygame.font.SysFont('Comic Sans MS', 22)
font_ranking = pygame.font.SysFont('Comic Sans MS', 28)

# Botones en panel izquierdo
boton_jugar = pygame.Rect(80, 350, 160, 45)
boton_salir = pygame.Rect(80, 415, 160, 45)

texto_boton_jugar = font_inicio.render('JUGAR', True, (0, 0, 0))
texto_boton_salir = font_inicio.render('SALIR', True, (0, 0, 0))

# Campo nombre del jugador
input_rect = pygame.Rect(50, 275, 220, 35)
nombre_jugador = ""
input_activo = False

# Ranking placeholder
ranking = ["1. Juan", "2. Diego", "3. Topicos"]

# Variables de movimiento
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
                input_activo = input_rect.collidepoint(event.pos)
                if boton_jugar.collidepoint(event.pos):
                    estado = "juego"
                if boton_salir.collidepoint(event.pos):
                    run = False

            if event.type == pygame.KEYDOWN and input_activo:
                if event.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif len(nombre_jugador) < 14:
                    nombre_jugador += event.unicode

        # Fondo
        ventana.fill(constantes.MORADO)

        # Panel izquierdo
        pygame.draw.rect(ventana, (40, 15, 75), (0, 0, 320, ALTO_VENTANA))

        # Logo Pac-Man (circulo amarillo)
        pygame.draw.circle(ventana, (255, 220, 0), (160, 130), 65)
        pygame.draw.polygon(ventana, (40, 15, 75), [(160, 130), (220, 90), (220, 170)])

        # Texto PACMAN
        txt_pacman = font_inicio.render('PACMAN', True, (255, 220, 0))
        ventana.blit(txt_pacman, (160 - txt_pacman.get_width() // 2, 210))

        # Etiqueta campo nombre
        txt_label = font_input.render('Nombre:', True, (255, 255, 255))
        ventana.blit(txt_label, (input_rect.x, input_rect.y - 25))

        # Campo nombre
        pygame.draw.rect(ventana, (0, 0, 0), input_rect)
        if input_activo:
            pygame.draw.rect(ventana, (255, 220, 0), input_rect, 2)
        else:
            pygame.draw.rect(ventana, (200, 200, 200), input_rect, 2)
        txt_nombre = font_input.render(nombre_jugador, True, (255, 255, 255))
        ventana.blit(txt_nombre, (input_rect.x + 5, input_rect.y + 6))

        # Botones
        pygame.draw.rect(ventana, (160, 160, 160), boton_jugar)
        pygame.draw.rect(ventana, (160, 160, 160), boton_salir)
        ventana.blit(texto_boton_jugar, texto_boton_jugar.get_rect(center=boton_jugar.center))
        ventana.blit(texto_boton_salir, texto_boton_salir.get_rect(center=boton_salir.center))

        # Linea divisoria
        pygame.draw.line(ventana, (0, 0, 0), (320, 0), (320, ALTO_VENTANA), 3)

        # Panel derecho - Ranking
        pygame.draw.rect(ventana, (60, 25, 100), (320, 0, ANCHO_VENTANA - 320, ALTO_VENTANA))

        txt_ranking = font_ranking.render('Ranking', True, (255, 255, 255))
        ventana.blit(txt_ranking, (400, 80))

        for i, linea in enumerate(ranking):
            txt_linea = font_input.render(linea, True, (255, 255, 255))
            ventana.blit(txt_linea, (420, 140 + i * 40))

    elif estado == "juego":
        reloj.tick(constantes.FPS)

        ventana.fill(constantes.COLOR_FONDO)

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
