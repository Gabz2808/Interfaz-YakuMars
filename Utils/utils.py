# utils.py

import pygame


class Utils:
    def __init__(self):
        # Definir las dimensiones de la pantalla
        self.screen_width = 1200
        self.screen_height = 600

        # Colores
        self.colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0),
            "indigo": (75, 0, 130),
            "violet": (238, 130, 238),
            "deep_pink": (255, 20, 147),
            "cyan": (0, 255, 255),
            "custom_color_1": (255, 255, 255),  # Blanco
        }

        # Duplicar los colores de cuadros
        self.COLORES_CUADROS = [
            self.colors["red"],
            self.colors["green"],
            self.colors["blue"],
            self.colors["yellow"],
            self.colors["orange"],
            self.colors["indigo"],
            self.colors["violet"],
            self.colors["deep_pink"],
            self.colors["cyan"],
            self.colors["custom_color_1"],
        ] * 2  # Duplicar para tener más opciones

        # Cargar las fuentes
        self.fonts = {
            "title_font": pygame.font.SysFont("Arial", 36, bold=True),
            "button_font": pygame.font.SysFont("Arial", 24),
            "text_font": pygame.font.SysFont("Arial", 18)
        }

        # Tamaño de los íconos
        self.icon_size = (50, 50)

        # Dimensiones de botones
        self.button_width = 150
        self.button_height = 50
        self.button_spacing = 20

    def get_color(self, color_name):
        """Método para obtener colores."""
        return self.colors.get(color_name, self.colors["white"])  # Blanco por defecto

    def get_font(self, font_name):
        """Método para obtener fuentes."""
        return self.fonts.get(font_name, self.fonts["text_font"])  # Fuente de texto por defecto
