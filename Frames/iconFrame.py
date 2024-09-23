# iconFrame.py
import pygame
from tkinter import messagebox
import tkinter as tk


class IconFrame:
    def __init__(self, screen, utils):
        self.screen = screen
        self.utils = utils

        # Cargar las imágenes de los íconos
        self.pause_icon = pygame.transform.scale(pygame.image.load(
            'src/pause_icon.png'), utils.icon_size)
        self.reset_icon = pygame.transform.scale(pygame.image.load(
            'src/reset_icon.png'), utils.icon_size)
        self.start_icon = pygame.transform.scale(pygame.image.load(
            'src/start_icon.png'), utils.icon_size)

        # Definir las posiciones de los botones (ahora íconos)
        self.pause_button_rect = pygame.Rect(
            (screen.get_width() - 3 * utils.button_width -
             2 * utils.button_spacing) // 2,
            screen.get_height() - utils.button_height - 20,  # Margen en la parte inferior
            utils.button_width, utils.button_height
        )
        self.reset_button_rect = pygame.Rect(
            self.pause_button_rect.right + utils.button_spacing,
            self.pause_button_rect.top, utils.button_width, utils.button_height
        )
        self.start_button_rect = pygame.Rect(
            self.reset_button_rect.right + utils.button_spacing,
            self.pause_button_rect.top, utils.button_width, utils.button_height
        )

        # Estado de los botones
        self.paused = False
        self.started = False

    def draw_icons(self):
        """Dibuja los íconos en sus respectivas posiciones."""
        self._draw_icon(self.pause_button_rect, self.pause_icon)
        self._draw_icon(self.reset_button_rect, self.reset_icon)
        self._draw_icon(self.start_button_rect, self.start_icon)

    def _draw_icon(self, rect, icon):
        """Dibuja un ícono en el rectángulo especificado."""
        icon_rect = icon.get_rect(center=rect.center)
        self.screen.blit(icon, icon_rect)

    def handle_event(self, event):
        """Gestiona los eventos de clic para los íconos."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button_rect.collidepoint(event.pos):
                self.paused = not self.paused
                self._mostrar_alerta(
                    "Alerta: sistema pausado" if self.paused else "Alerta: sistema reanudado")
            elif self.reset_button_rect.collidepoint(event.pos):
                self._mostrar_alerta("Alerta: sistema reiniciado")
            elif self.start_button_rect.collidepoint(event.pos):
                self.started = True
                self.paused = False
                self._mostrar_alerta("Alerta: sistema reanudado")

    def _mostrar_alerta(self, message):
        """Muestra una ventana de alerta."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        messagebox.showinfo("Alerta", message)
        root.destroy()  # Cerrar la ventana después de la alerta
