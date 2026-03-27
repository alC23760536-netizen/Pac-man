import constantes
import pygame
from personaje import Personaje

from constantes import ANCHO_VENTANA, ALTO_VENTANA

pacman = Personaje(350, 350)

pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Pacman')

# Fuentes
font_titulo = pygame.font.SysFont('Comic Sans MS', 60)
font_inicio = pygame.font.SysFont('Comic Sans MS', 30)
font_input = pygame.font.SysFont('Comic Sans MS', 24)
font_label = pygame.font.SysFont('Comic Sans MS', 20)

# Centro de la ventana
cx = ANCHO_VENTANA // 2
cy = ALTO_VENTANA // 2

# Botones centrados
boton_jugar = pygame.Rect(cx - 100, cy + 20,  200, 50)
boton_salir = pygame.Rect(cx - 100, cy + 90,  200, 50)

texto_boton_jugar = font_inicio.render('Jugar', True, (255, 255, 255))
texto_boton_salir = font_inicio.render('Salir', True, (255, 255, 255))

# Campo de nombre del jugador
input_rect = pygame.Rect(cx - 150, cy - 60, 300, 40)
nombre_jugador = ""       # texto que escribe el usuario
input_activo = False      # si el campo está seleccionado

# Variables de movimiento
mover_arriba = mover_abajo = mover_derecha = mover_izquierda = False

reloj = pygame.time.Clock()
estado = "menu"
run = True

while run:

    if estado == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Activar / desactivar el campo de texto al hacer clic
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_activo = input_rect.collidepoint(event.pos)

                if boton_jugar.collidepoint(event.pos):
                    estado = "juego"
                if boton_salir.collidepoint(event.pos):
                    run = False

            # Escribir en el campo de nombre
            if event.type == pygame.KEYDOWN and input_activo:
                if event.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif len(nombre_jugador) < 16:          # límite de caracteres
                    nombre_jugador += event.unicode

        # --- Dibujar menú ---
        ventana.fill(constantes.MORADO)

        # Título
        titulo = font_titulo.render('PAC-MAN', True, (255, 255, 0))
        ventana.blit(titulo, titulo.get_rect(center=(cx, cy - 150)))

        # Etiqueta del campo
        label = font_label.render('Nombre del jugador:', True, (255, 255, 255))
        ventana.blit(label, (input_rect.x, input_rect.y - 25))

        # Campo de texto
        color_borde = (255, 255, 0) if input_activo else (200, 200, 200)
        pygame.draw.rect(ventana, (0, 0, 0), input_rect, border_radius=6)
        pygame.draw.rect(ventana, color_borde, input_rect, 2, border_radius=6)
        texto_nombre = font_input.render(nombre_jugador, True, (255, 255, 255))
        ventana.blit(texto_nombre, (input_rect.x + 8, input_rect.y + 8))

        # Botones
        pygame.draw.rect(ventana, (0, 0, 0), boton_jugar, border_radius=8)
        pygame.draw.rect(ventana, (255, 255, 0), boton_jugar, 2, border_radius=8)
        ventana.blit(texto_boton_jugar,
                     texto_boton_jugar.get_rect(center=boton_jugar.center))

        pygame.draw.rect(ventana, (0, 0, 0), boton_salir, border_radius=8)
        pygame.draw.rect(ventana, (255, 255, 0), boton_salir, 2, border_radius=8)
        ventana.blit(texto_boton_salir,
                     texto_boton_salir.get_rect(center=boton_salir.center))

    elif estado == "juego":
        reloj.tick(constantes.FPS)
        ventana.fill(constantes.COLOR_FONDO)

        delta_x = 0
        delta_y = 0

        if mover_derecha:
            delta_x = 5
        if mover_izquierda:
            delta_x = -5
        if mover_abajo:
            delta_y = 5
        if mover_arriba:
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
