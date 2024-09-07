import pygame


class JsonResponseFrame:
    def __init__(self, json_data):
        self.width = 350
        self.height = 400
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))  # Fondo negro
        self.font = pygame.font.SysFont(None, 24)

        # Ahora recibimos los datos del JSON
        self.text_lines = self.parse_json_to_text(json_data)

    def parse_json_to_text(self, json_data):
        """Convierte un diccionario JSON en una lista de líneas de texto."""
        text_lines = []
        for key, value in json_data.items():
            text_lines.append(f"{key}: {value}")
        return text_lines

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
        for i, line in enumerate(self.text_lines):
            text_surface = self.font.render(
                line, True, (35, 213, 11))  # Texto verde
            # Ajusta la posición del texto
            screen.blit(text_surface, (x + 10, y + 10 + i * 20))
