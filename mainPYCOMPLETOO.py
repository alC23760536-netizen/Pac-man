import constantes
import pygame
import random
import math
from personaje import Personaje
from constantes import ANCHO_VENTANA, ALTO_VENTANA

pacman = Personaje(350, 350)

pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Pacman')

# Fuentes pixel/retro
font_titulo    = pygame.font.SysFont('Courier New', 28, bold=True)
font_boton     = pygame.font.SysFont('Courier New', 22, bold=True)
font_ranking   = pygame.font.SysFont('Courier New', 26, bold=True)
font_rank_item = pygame.font.SysFont('Courier New', 18)
font_input     = pygame.font.SysFont('Courier New', 18)
font_label     = pygame.font.SysFont('Courier New', 16)

# Colores
MORADO_OSCURO  = (15, 5, 35)
MORADO_PANEL   = (50, 20, 90)
MORADO_RANKING = (70, 30, 110)
AMARILLO       = (255, 220, 0)
BLANCO         = (255, 255, 255)
GRIS_BOTON     = (140, 140, 140)
GRIS_BOTON_H   = (190, 190, 190)
NEGRO          = (0, 0, 0)

# Estrellas de fondo
random.seed(42)
estrellas = [(random.randint(0, ANCHO_VENTANA), random.randint(0, ALTO_VENTANA),
              random.randint(1, 3)) for _ in range(150)]

# Layout
PANEL_DIV = 350

# Botones (centrados en panel izquierdo)
boton_jugar = pygame.Rect(175 - 70, 350, 140, 42)
boton_salir = pygame.Rect(175 - 70, 410, 140, 42)

# Campo de nombre del jugador
input_rect     = pygame.Rect(175 - 100, 278, 200, 32)
nombre_jugador = ""
input_activo   = False

# Ranking placeholder
ranking = [("Juan", 0), ("Diego", 0), ("Topicos", 0)]

# Variables de movimiento
mover_arriba = mover_abajo = mover_derecha = mover_izquierda = False

reloj  = pygame.time.Clock()
estado = "menu"
run    = True


def dibujar_pacman_logo(surface, cx, cy, radio):
    """Dibuja el icono de Pac-Man (circulo con boca abierta)."""
    boca = 35  # grados de apertura
    puntos = [(cx, cy)]
    for ang in range(boca, 361 - boca, 2):
        rad = math.radians(ang)
        px = cx + int(radio * math.cos(rad))
        py = cy - int(radio * math.sin(rad))
        puntos.append((px, py))
    pygame.draw.polygon(surface, AMARILLO, puntos)


def dibujar_estrellas(surface):
    for x, y, brillo in estrellas:
        c = brillo * 70
        pygame.draw.circle(surface, (c, c, c), (x, y), 1)


while run:
    reloj.tick(constantes.FPS)

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

        # ── Fondo ──────────────────────────────────────────────────
        ventana.fill(MORADO_OSCURO)
        dibujar_estrellas(ventana)

        # ── Panel izquierdo ────────────────────────────────────────
        panel_izq = pygame.Surface((PANEL_DIV, ALTO_VENTANA), pygame.SRCALPHA)
        panel_izq.fill((50, 20, 90, 220))
        ventana.blit(panel_izq, (0, 0))

        # Logo Pac-Man
        dibujar_pacman_logo(ventana, 175, 135, 65)

        # Texto PACMAN
        txt_pacman = font_titulo.render('PACMAN', True, AMARILLO)
        ventana.blit(txt_pacman, txt_pacman.get_rect(center=(175, 220)))

        # Etiqueta y campo nombre
        label_txt = font_label.render('Nombre del jugador:', True, BLANCO)
        ventana.blit(label_txt, (input_rect.x, input_rect.y - 20))
        color_borde = AMARILLO if input_activo else GRIS_BOTON
        pygame.draw.rect(ventana, NEGRO, input_rect, border_radius=4)
        pygame.draw.rect(ventana, color_borde, input_rect, 2, border_radius=4)
        txt_nombre = font_input.render(nombre_jugador, True, BLANCO)
        ventana.blit(txt_nombre, (input_rect.x + 6, input_rect.y + 7))

        # Botones con hover
        mouse = pygame.mouse.get_pos()
        c_jugar = GRIS_BOTON_H if boton_jugar.collidepoint(mouse) else GRIS_BOTON
        c_salir = GRIS_BOTON_H if boton_salir.collidepoint(mouse) else GRIS_BOTON
        pygame.draw.rect(ventana, c_jugar, boton_jugar, border_radius=5)
        pygame.draw.rect(ventana, c_salir, boton_salir, border_radius=5)
        txt_jugar = font_boton.render('JUGAR', True, NEGRO)
        txt_salir = font_boton.render('SALIR', True, NEGRO)
        ventana.blit(txt_jugar, txt_jugar.get_rect(center=boton_jugar.center))
        ventana.blit(txt_salir, txt_salir.get_rect(center=boton_salir.center))

        # ── Línea divisoria ────────────────────────────────────────
        pygame.draw.line(ventana, NEGRO, (PANEL_DIV, 0), (PANEL_DIV, ALTO_VENTANA), 3)

        # ── Panel derecho (Ranking) ────────────────────────────────
        panel_der = pygame.Surface((ANCHO_VENTANA - PANEL_DIV, ALTO_VENTANA), pygame.SRCALPHA)
        panel_der.fill((70, 30, 110, 200))
        ventana.blit(panel_der, (PANEL_DIV, 0))

        txt_ranking = font_ranking.render('Ranking', True, BLANCO)
        ventana.blit(txt_ranking, (PANEL_DIV + 40, 90))

        for i, (nombre, puntaje) in enumerate(ranking):
            linea = font_rank_item.render(f'{i+1}. {nombre}', True, BLANCO)
            ventana.blit(linea, (PANEL_DIV + 60, 150 + i * 38))

    elif estado == "juego":
        ventana.fill(constantes.COLOR_FONDO)

        delta_x = 0
        delta_y = 0
        if mover_derecha:   delta_x =  5
        if mover_izquierda: delta_x = -5
        if mover_abajo:     delta_y =  5
        if mover_arriba:    delta_y = -5

        pacman.movimiento(delta_x, delta_y)
        pacman.dibujar(ventana)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: mover_izquierda = True
                if event.key == pygame.K_d: mover_derecha   = True
                if event.key == pygame.K_w: mover_arriba    = True
                if event.key == pygame.K_s: mover_abajo     = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: mover_izquierda = False
                if event.key == pygame.K_d: mover_derecha   = False
                if event.key == pygame.K_w: mover_arriba    = False
                if event.key == pygame.K_s: mover_abajo     = False

    pygame.display.update()
