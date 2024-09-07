import pygame
import random
import math


class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(1, 3)
        self.size = random.randint(2, 5)
        self.color = (random.randint(100, 255), random.randint(
            100, 255), random.randint(100, 255))

    def move(self):
        self.y -= self.speed  # Mover hacia arriba
        self.x += random.choice([-1, 1])  # Mover ligeramente hacia los lados

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)


class Animations:
    def __init__(self):
        self.image_x = 50
        self.image_speed = 2  # Velocidad de movimiento de la imagen
        self.terminal_y = 500
        self.terminal_speed = 1  # Velocidad de movimiento vertical del texto
        self.angle = 0  # Inicializa el ángulo para el círculo giratorio
        self.particulas = [Particula(random.randint(50, 1000), 500)
                           for _ in range(20)]  # Crear partículas
        self.text_progress = {}  # Diccionario para controlar el progreso de texto

    def type_writer_text(self, screen, text, pos, key):
        if key not in self.text_progress:
            self.text_progress[key] = 0

        if self.text_progress[key] < len(text):
            self.text_progress[key] += 1

        rendered_text = text[:self.text_progress[key]]
        text_surface = pygame.font.Font(None, 36).render(
            rendered_text, True, (35, 213, 11))
        screen.blit(text_surface, pos)

    def scroll_terminal_text(self, screen, frame, screen_height, position):
        self.terminal_y -= self.terminal_speed
        if self.terminal_y < 40:
            self.terminal_y = screen_height
        frame.draw(screen, position, self.terminal_y)
