import pygame
from Frames.Frame import Frame
from Utils.utils import Utils  # Importamos la clase Utils


class PlantaFrame(Frame):
    def __init__(self, screen, rect, data):
        image_path = "src/planta.jpg"
        title = "Imagen de Planta"
        data_key = "Turbidez"
        data_value = data.get(data_key, "N/A")

        # Inicializa la clase padre Frame
        super().__init__(screen, rect, title, data_key, data_value)

        # Instancia de Utils para utilizar colores y otros recursos
        self.utils = Utils()

        # Cargar la imagen de planta y ajustarla al tamaño del rectángulo
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            self.image, (rect.width, rect.height))

        # Inicializar lista para almacenar los rectángulos resaltados
        self.highlight_rects = []

        # Controlar parpadeo
        self.blink_time = 500  # Duración de visibilidad en ms (0.5 segundos)
        self.last_blink = pygame.time.get_ticks()  # Última vez que parpadeó
        self.visible = True  # Controla si el rectángulo es visible

        # Llamar a los métodos que crean los rectángulos
        self.create_center_rectangle()
        self.create_green_rectangle()
        self.create_blue_rectangle()
        self.create_yellow_rectangle()

    def create_center_rectangle(self):
        """Crear el rectángulo central rojo."""
        rect_width = 125
        rect_height = 80
        center_x = 185
        center_y = 260
        highlight_rect = pygame.Rect(
            center_x, center_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("red")))

    def create_green_rectangle(self):
        """Crear el rectángulo verde."""
        rect_width = 60
        rect_height = 80
        green_x = 700
        green_y = 200
        highlight_rect = pygame.Rect(green_x, green_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("green")))

    def create_blue_rectangle(self):
        """Crear el rectángulo azul."""
        rect_width = 140
        rect_height = 150
        blue_x = 366
        blue_y = 193
        highlight_rect = pygame.Rect(blue_x, blue_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("blue")))

    def create_yellow_rectangle(self):
        """Crear el rectángulo amarillo."""
        rect_width = 117
        rect_height = 170
        yellow_x = 560
        yellow_y = 180
        highlight_rect = pygame.Rect(
            yellow_x, yellow_y, rect_width, rect_height)
        self.highlight_rects.append(
            (highlight_rect, self.utils.get_color("yellow")))

    def draw(self):
        """Dibuja la imagen, los rectángulos resaltados, y el contenido del frame."""
        # Dibuja el marco y el contenido de la clase padre
        super().draw()

        # Dibuja la imagen dentro del rectángulo
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        # Control del parpadeo (intercala visibilidad)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink >= self.blink_time:
            self.visible = not self.visible  # Alternar visibilidad
            self.last_blink = current_time  # Reiniciar el temporizador

        # Solo dibujar los rectángulos si son visibles
        if self.visible:
            for highlight_rect, color in self.highlight_rects:
                # Crear una superficie temporal con transparencia (usar canal alfa)
                transparent_surface = pygame.Surface(
                    (highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)

                # Rellenar la superficie con color semitransparente (RGBA: color + transparencia)
                # 128 es el valor de la transparencia (50%)
                transparent_surface.fill((*color, 128))

                # Dibujar la superficie sobre la pantalla en la posición del rectángulo
                self.screen.blit(transparent_surface,
                                 (highlight_rect.x, highlight_rect.y))

                # Dibujar el borde sólido alrededor del rectángulo
                # Borde de grosor 5
                pygame.draw.rect(self.screen, color, highlight_rect, 5)
