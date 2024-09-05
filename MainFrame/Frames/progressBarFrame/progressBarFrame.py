import pygame
import sys

# Clase para la barra de progreso


class ProgressBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.progress = 0  # El progreso es un valor entre 0 y 100

    def draw(self, screen):
        # Dibujar la barra de fondo (gris)
        pygame.draw.rect(screen, (169, 169, 169),
                         (self.x, self.y, self.width, self.height))
        # Dibujar la barra de progreso (verde)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y,
                         self.width * (self.progress / 100), self.height))

    def update(self, value):
        # Actualizar el progreso
        # Asegura que el progreso esté entre 0 y 100
        self.progress = min(max(value, 0), 100)
