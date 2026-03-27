import tkinter as tk
import subprocess
import sys
import os

import constantes
import pygame
from personaje import Personaje
from constantes import ANCHO_VENTANA, ALTO_VENTANA


# ================================================================
#  CLASE MENU (tkinter)
# ================================================================
class MenuPacman:

    def __init__(self):
        self.COLOR_FONDO_IZQ  = "#1a0a2e"
        self.COLOR_FONDO_DER  = "#2d1060"
        self.COLOR_AMARILLO   = "#f5c800"
        self.COLOR_BLANCO     = "#ffffff"
        self.COLOR_GRIS_BTN   = "#888888"
        self.COLOR_GRIS_HOVER = "#aaaaaa"
        self.COLOR_NEGRO      = "#000000"
        self.COLOR_LINEA      = "#0d0520"
        self.COLOR_ESTRELLA   = "#555577"

        self.ranking = ["1. Juan", "2. Diego", "3. Topicos"]
        self.iniciar_juego = False  # bandera para saber si se presionó JUGAR

        self.iniciar_ventana()

    def iniciar_ventana(self):
        """Configura la ventana principal y lanza el menú."""
        self.ventana = tk.Tk()
        self.ventana.title("PAC-MAN")
        self.ventana.geometry("800x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=self.COLOR_FONDO_IZQ)

        self.crear_canvas()
        self.dibujar_panel_izquierdo()
        self.dibujar_panel_derecho()
        self.dibujar_logo()
        self.dibujar_titulo()
        self.dibujar_botones()
        self.dibujar_ranking()

        self.ventana.mainloop()

    def crear_canvas(self):
        """Crea el canvas principal que ocupa toda la ventana."""
        self.canvas = tk.Canvas(
            self.ventana,
            width=800, height=500,
            bg=self.COLOR_FONDO_IZQ,
            highlightthickness=0
        )
        self.canvas.pack()

    def dibujar_panel_izquierdo(self):
        """Dibuja el panel oscuro del lado izquierdo."""
        self.canvas.create_rectangle(
            0, 0, 360, 500,
            fill=self.COLOR_FONDO_IZQ,
            outline=""
        )
        estrellas = [
            (30, 40), (80, 120), (15, 200), (50, 350),
            (200, 30), (310, 90), (270, 420), (100, 460),
            (340, 280), (160, 480)
        ]
        for x, y in estrellas:
            self.canvas.create_text(
                x, y, text="*",
                fill=self.COLOR_ESTRELLA,
                font=("Courier", 10, "bold")
            )

    def dibujar_panel_derecho(self):
        """Dibuja el panel morado del lado derecho."""
        self.canvas.create_rectangle(
            360, 0, 800, 500,
            fill=self.COLOR_FONDO_DER,
            outline=""
        )
        self.canvas.create_line(
            360, 0, 360, 500,
            fill=self.COLOR_LINEA,
            width=3
        )
        estrellas_der = [
            (400, 50), (500, 30), (650, 70), (750, 120),
            (420, 200), (700, 250), (550, 380), (780, 450),
            (470, 460), (630, 130)
        ]
        for x, y in estrellas_der:
            self.canvas.create_text(
                x, y, text="*",
                fill=self.COLOR_ESTRELLA,
                font=("Courier", 10, "bold")
            )

    def dibujar_logo(self):
        """Dibuja el logo de Pac-Man (arco amarillo)."""
        self.canvas.create_arc(
            100, 50, 240, 190,
            start=35, extent=290,
            fill=self.COLOR_AMARILLO,
            outline=""
        )

    def dibujar_titulo(self):
        """Dibuja el texto PACMAN debajo del logo."""
        self.canvas.create_text(
            175, 215,
            text="PACMAN",
            fill=self.COLOR_AMARILLO,
            font=("Courier", 22, "bold")
        )

    def dibujar_botones(self):
        """Crea los botones JUGAR y SALIR."""
        self._crear_boton(175, 285, "JUGAR", self.accion_jugar)
        self._crear_boton(175, 345, "SALIR", self.accion_salir)

    def _crear_boton(self, x, y, texto, comando):
        """Crea un botón centrado en (x, y) con estilo retro."""
        btn = tk.Button(
            self.canvas,
            text=texto,
            command=comando,
            font=("Courier", 14, "bold"),
            bg=self.COLOR_GRIS_BTN,
            fg=self.COLOR_NEGRO,
            activebackground=self.COLOR_GRIS_HOVER,
            activeforeground=self.COLOR_NEGRO,
            relief="flat",
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.COLOR_GRIS_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.COLOR_GRIS_BTN))
        self.canvas.create_window(x, y, window=btn, width=160, height=42)

    def dibujar_ranking(self):
        """Dibuja la sección de Ranking en el panel derecho."""
        self.canvas.create_text(
            490, 100,
            text="Ranking",
            fill=self.COLOR_BLANCO,
            font=("Courier", 26, "bold"),
            anchor="w"
        )
        for i, jugador in enumerate(self.ranking):
            self.canvas.create_text(
                510, 160 + i * 45,
                text=jugador,
                fill=self.COLOR_BLANCO,
                font=("Courier", 16),
                anchor="w"
            )

    def accion_jugar(self):
        """Cierra el menú y activa la bandera para iniciar el juego."""
        self.iniciar_juego = True
        self.ventana.destroy()

    def accion_salir(self):
        """Cierra la aplicación."""
        self.iniciar_juego = False
        self.ventana.destroy()


# ================================================================
#  FUNCIÓN JUEGO (pygame)
# ================================================================
def correr_juego():
    """Inicializa y ejecuta el juego Pac-Man con pygame."""
    pacman = Personaje(350, 350)

    pygame.init()
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption('Pacman')

    font_inicio = pygame.font.SysFont('Comic Sans MS', 30)
    font_input  = pygame.font.SysFont('Comic Sans MS', 22)
    font_ranking = pygame.font.SysFont('Comic Sans MS', 28)

    reloj = pygame.time.Clock()

    mover_arriba    = False
    mover_abajo     = False
    mover_derecha   = False
    mover_izquierda = False

    run = True
    while run:
        reloj.tick(constantes.FPS)

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

    pygame.quit()


# ================================================================
#  PUNTO DE ENTRADA
# ================================================================
if __name__ == "__main__":
    # 1. Mostrar el menú tkinter
    menu = MenuPacman()

    # 2. Si el jugador presionó JUGAR, lanzar el juego pygame
    if menu.iniciar_juego:
        correr_juego()
