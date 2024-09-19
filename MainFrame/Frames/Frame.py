import pygame


class Frame:
    def __init__(self, screen, rect, title, data_key, data_value):
        self.screen = screen
        self.rect = rect
        self.title = title
        self.data_key = data_key
        self.data_value = data_value
        self.font = pygame.font.Font(None, 36)
        self.data = {}  # Asegúrate de que data está inicializado aquí

    def draw(self):
        # Método de dibujo base, puede ser implementado en subclases
        pass
