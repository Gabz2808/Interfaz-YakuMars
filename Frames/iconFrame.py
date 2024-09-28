import pygame


class IconFrame:
    def __init__(self, screen, utils, reset_app_callback):
        self.screen = screen
        self.utils = utils
        self.reset_app_callback = reset_app_callback

        # Cargar las imágenes de los íconos
        self.pause_icon = pygame.transform.scale(pygame.image.load(
            'src/pause_icon.png'), utils.icon_size)
        self.start_icon = pygame.transform.scale(pygame.image.load(
            'src/start_icon.png'), utils.icon_size)
        self.reset_icon = pygame.transform.scale(pygame.image.load(
            'src/reset_icon.png'), utils.icon_size)

        # Obtener las dimensiones de la pantalla
        screen_rect = self.screen.get_rect()

        # Calcular la posición inicial centrada en la parte inferior de la pantalla
        center_y = screen_rect.centery + 25  # Ajustar según sea necesario
        total_width = (utils.button_width * 3) + (utils.button_spacing * 2)

        # Definir las posiciones de los botones (ahora íconos) centrados en la pantalla
        self.pause_button_rect = pygame.Rect(
            screen_rect.centerx - total_width // 2,
            center_y,
            utils.button_width, utils.button_height
        )
        self.start_button_rect = pygame.Rect(
            self.pause_button_rect.right + utils.button_spacing,
            self.pause_button_rect.top, utils.button_width, utils.button_height
        )
        self.reset_button_rect = pygame.Rect(
            self.start_button_rect.right + utils.button_spacing,
            self.pause_button_rect.top, utils.button_width, utils.button_height
        )

        # Estado de los botones
        self.paused = False
        self.started = False

        # Fuente para mensajes
        self.font = pygame.font.SysFont(None, 36)
        self.message = ""

    def draw_icons(self):
        """Dibuja los íconos en sus respectivas posiciones."""
        self._draw_icon(self.pause_button_rect, self.pause_icon)
        self._draw_icon(self.start_button_rect, self.start_icon)
        self._draw_icon(self.reset_button_rect, self.reset_icon)

        # Mostrar el mensaje en la pantalla si existe
        if self.message:
            self._draw_message()

    def _draw_icon(self, rect, icon):
        """Dibuja un ícono en el rectángulo especificado."""
        icon_rect = icon.get_rect(center=rect.center)
        self.screen.blit(icon, icon_rect)

    def handle_event(self, event):
        """Gestiona los eventos de clic para los íconos."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button_rect.collidepoint(event.pos):
                self.paused = not self.paused
                self.message = "Sistema pausado" if self.paused else "Sistema reanudado"
            elif self.start_button_rect.collidepoint(event.pos):
                self.started = True
                self.paused = False
                self.message = "Continuando el sistema"
            elif self.reset_button_rect.collidepoint(event.pos):
                self.reset_app_callback()  # Llamar a la función de reinicio
                self.message = "Sistema reiniciado"
                self.started = False
                self.paused = False

    def _draw_message(self):
        """Dibuja el mensaje en la pantalla."""
        message_surface = self.font.render(
            self.message, True, (255, 0, 0))  # Texto en rojo
        message_rect = message_surface.get_rect(
            # Centrado en la parte superior
            center=(self.screen.get_width() // 2, 50))
        self.screen.blit(message_surface, message_rect)

    def is_paused(self):
        """Verifica si el sistema está pausado."""
        return self.paused

    def is_started(self):
        """Verifica si el sistema ha comenzado."""
        return self.started
