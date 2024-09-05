import pygame
import sys

# Class for the Terminal Process Frame


class ProcessFrame:
    def __init__(self):
        self.width = 250
        self.height = 150
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))  # Light blue background
        self.font = pygame.font.SysFont(None, 24)
        self.text = [
            "Terminal cargando procesos:",
            "Proceso1: TRUE,",
            "Proceso2: FALSE...",
            "Proceso3: Waiting..."
        ]

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
        for i, line in enumerate(self.text):
            text_surface = self.font.render(
                line, True, (35, 213, 11))  # Black text
            screen.blit(text_surface, (x + 10, y + 10 + i * 25))
