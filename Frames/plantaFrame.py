import pygame
from Frames.Frame import Frame


class PlantaFrame(Frame):
    def __init__(self, screen, rect, data):
        image_path = "src/planta.jpg"
        # Inicializa la clase padre Frame
        title = "Imagen de Planta"
        data_key = "Turbidez"
        data_value = data.get(data_key, "N/A")
        super().__init__(screen, rect, title, data_key, data_value)

        # Cargar la imagen de planta
        # Cargar imagen desde el archivo
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            # Ajustar tamaño al rectángulo
            self.image, (rect.width, rect.height))

    def draw(self):
        # Dibuja el marco y el contenido de la clase padre (puedes definir esto en la clase Frame)
        super().draw()

        # Dibuja la imagen dentro del rectángulo proporcionado
        # Ubicar la imagen en el rectángulo
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        # También puedes dibujar el texto del título y cualquier otro dato en esta área si es necesario.
