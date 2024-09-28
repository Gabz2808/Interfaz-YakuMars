import pygame
from Frames.Frame import Frame
from Utils.utils import Utils  # Importamos la clase Utils


class PlantaFrame(Frame):
    def __init__(self, screen, rect, data):
        image_path = "src/planta.jpg"
        title = "Imagen de Planta"
        data_key = "Turbidez"
        data_value = data.get(data_key, "N/A")

        super().__init__(screen, rect, title, data_key, data_value)

        self.utils = Utils()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            self.image, (rect.width, rect.height))
        self.highlight_rects = []
        self.blink_time = 400
        self.last_blink = pygame.time.get_ticks()
        self.visible = True

        # Llamar a los métodos que crean los rectángulos
        self.pretratamiento()
        self.electrocuagulacion()
        self.aireacion()
        self.ultrafiltración()
        self.aguaLimpia()  # Llamar al método para crear el nuevo rectángulo celeste

        # Inicializa la visibilidad de los rectángulos
        self.rect_visibility = [False] * len(self.highlight_rects)

    def pretratamiento(self):
        """Crear el rectángulo central rojo."""
        rect_width = 125
        rect_height = 80
        center_x = 185
        center_y = 260
        highlight_rect = pygame.Rect(
            center_x, center_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("red")))

    def ultrafiltración(self):
        """Crear el rectángulo verde."""
        rect_width = 60
        rect_height = 80
        green_x = 700
        green_y = 200
        highlight_rect = pygame.Rect(green_x, green_y, rect_width, rect_height)
        self.highlight_rects.append(
            # Color verde para ultrafiltración
            (highlight_rect, self.utils.get_color("green")))

    def electrocuagulacion(self):
        """Crear el rectángulo azul."""
        rect_width = 140
        rect_height = 150
        blue_x = 366
        blue_y = 193
        highlight_rect = pygame.Rect(blue_x, blue_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("blue")))

    def aireacion(self):
        """Crear el rectángulo amarillo."""
        rect_width = 117
        rect_height = 170
        yellow_x = 560
        yellow_y = 180
        highlight_rect = pygame.Rect(
            yellow_x, yellow_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("yellow")))

    def aguaLimpia(self):
        """Crear el rectángulo celeste debajo del rectángulo verde."""
        rect_width = 100
        rect_height = 50
        celeste_x = 680  # La misma posición x que el rectángulo verde
        celeste_y = 280  # Posición y debajo del rectángulo verde
        highlight_rect = pygame.Rect(
            celeste_x, celeste_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("lightblue")))  # Color celeste

    def update_visibility(self, current_index):
        """Actualizar la visibilidad de los rectángulos según el índice actual."""

        if current_index < len(self.highlight_rects):
            # Inicializamos la visibilidad con todo en False
            self.rect_visibility = [False] * len(self.highlight_rects)

            # Configuración de visibilidad según el índice actual
            if current_index == 0:  # Rojo
                self.rect_visibility[0] = True
            elif current_index == 1:  # Azul
                self.rect_visibility[1] = True
            elif current_index == 2:  # Amarillo
                self.rect_visibility[2] = True
            elif current_index in (3, 4, 5):  # Verde en los procesos 3, 4 y 5
                self.rect_visibility[3] = True  # Mantener el verde visible

            else:
                # Desactiva todos si el índice es inválido
                self.rect_visibility = [False] * len(self.highlight_rects)

    def draw(self):
        """Dibuja la imagen, los rectángulos resaltados, y el contenido del frame."""
        super().draw()
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        # Control del parpadeo
        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink > self.blink_time:
            self.visible = not self.visible
            self.last_blink = current_time

        for i, (highlight_rect, color) in enumerate(self.highlight_rects):
            if self.rect_visibility[i] and self.visible:
                # Crear superficie transparente para el rectángulo
                transparent_surface = pygame.Surface(
                    (highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
                # Color con transparencia
                transparent_surface.fill((*color, 128))
                self.screen.blit(transparent_surface,
                                 (highlight_rect.x, highlight_rect.y))
                # Dibuja el borde del rectángulo
                pygame.draw.rect(self.screen, color, highlight_rect, 5)

    def update_data(self, data):
        """Update the data displayed in the frame."""
        data_key = "Turbidez"
        self.data_value = data.get(data_key, "N/A")
