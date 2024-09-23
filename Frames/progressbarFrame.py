import pygame
import pygame.freetype
from Frames.Frame import Frame
from Data.processQueue import ProcessQueue


class BarraProgresoFrame:
    def __init__(self, screen, rect, data):
        data_key = "pH"
        data_value = data.get(data_key, "N/A")
        self.screen = screen
        self.rect = rect
        self.title = "Barra de Progreso"
        self.data_key = data_key
        self.data_value = data_value
        self.process_queue = ProcessQueue()
        self.font = pygame.freetype.SysFont('Arial', 24)
        # Color azul para la barra de progreso
        self.progress_color = (0, 102, 204)
        self.text_color = (0, 0, 0)  # Color negro para el texto
        self.progress_width = 0

    def draw(self):
        # Draw the frame background (transparent)
        pygame.draw.rect(self.screen, (255, 255, 255, 0), self.rect)

        # Draw the progress bar filling the entire width
        self.update_progress()
        pygame.draw.rect(self.screen, self.progress_color, pygame.Rect(
            self.rect.x, self.rect.y, self.rect.width, 30), border_radius=5)

        # Draw the progress percentage
        total_progress = self.calculate_progress_percentage()
        self.font.render_to(self.screen, (self.rect.x + 10, self.rect.y + 10),
                            f"Progreso: {total_progress:.2f}%", self.text_color)

    def update_progress(self):
        total_progress = self.calculate_progress_percentage()
        self.progress_width = (total_progress / 100) * self.rect.width

    def calculate_progress_percentage(self):
        return self.process_queue.current_step / self.process_queue.total_steps * 100 if self.process_queue.total_steps > 0 else 0

    def set_process_queue(self, process_queue):
        self.process_queue = process_queue
        self.process_queue.total_steps = len(self.process_queue.queue)

    def update_from_terminal(self, terminal_frame):
        progress_percentage = terminal_frame.get_progress_percentage()
        self.process_queue.current_step = int(
            (progress_percentage / 100) * self.process_queue.total_steps)
        self.update_progress()
