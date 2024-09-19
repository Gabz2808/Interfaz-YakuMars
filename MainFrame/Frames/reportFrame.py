import pygame
import pygame.freetype
from Data.processQueue import ProcessQueue
from Data.sampleData import ProcesosNecesarios, DataGenerator
import time


class ReporteFrame:
    def __init__(self, screen, rect, data):
        self.screen = screen
        self.rect = rect
        self.data = data
        self.font = pygame.freetype.SysFont(
            'Verdana', 14)  # Tamaño de letra reducido
        self.title_font = pygame.freetype.SysFont(
            'Verdana', 18, bold=True)  # Tamaño de letra reducido
        self.background_color = (240, 240, 240)
        self.entry_background_color = (255, 255, 255)
        self.entry_border_color = (200, 200, 200)
        self.text_color = (0, 0, 0)
        self.title_color = (0, 0, 0)
        self.entry_height = 30  # Altura de entrada ajustada
        self.history_limit = 7  # Limitado a 7 procesos
        self.max_frame_width = self.rect.width - 20
        self.max_frame_height = (self.rect.height - 60) // 2

        # Define maximum height for the history frame content
        self.max_history_height = self.max_frame_height - 10  # Adjust for margins

        self.data_generator = DataGenerator()
        self.procesos_necesarios = ProcesosNecesarios()

        self.datos = self.data_generator.generar_datos_random()
        self.tratamientos_necesarios, self.ajustes = self.procesos_necesarios.evaluar_tratamientos_necesarios(
            self.datos)

        self.tratamientos_necesarios_list = [
            f"{param}: {'Sí' if necesita_tratamiento else 'No'}"
            for param, necesita_tratamiento in self.tratamientos_necesarios.items() if necesita_tratamiento
        ]

        self.ajustes_list = [
            f"{param}: Ajuste necesario de {ajuste:.2f}"
            for param, ajuste in self.ajustes.items()
        ]

        self.process_queue = ProcessQueue()
        self.current_process_index = 0
        self.processing = False
        self.start_time = None
        self.history = []
        self.post_process_descriptions = []

        if self.tratamientos_necesarios_list:
            self.process_queue.queue = self.tratamientos_necesarios_list
            self.process_queue.total_steps = len(
                self.tratamientos_necesarios_list)
            self.process_queue.current_step = 0
            self.processing = True
            self.start_time = time.time()
            self.add_to_history(
                f"[{time.strftime('%H:%M:%S')}] Proceso 1: Iniciado")

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.rect)

        section_height = min(self.max_frame_height,
                             (self.rect.height - 60) // 2)

        history_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 50, self.max_frame_width, section_height)
        adjustments_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 50 + section_height + 10, self.max_frame_width, section_height)

        self.title_font.render_to(
            self.screen, (self.rect.x + 10, self.rect.y + 10), "Reporte de Progreso", self.title_color)

        self.draw_history(history_rect)
        self.draw_adjustments(adjustments_rect)

        if self.processing:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 2:
                self.complete_current_process()

    def draw_history(self, rect):
        pygame.draw.rect(self.screen, self.background_color, rect)
        y_offset = rect.y + 5

        # Draw history entries
        visible_history_entries = self.history[-self.history_limit:]
        for entry in visible_history_entries:
            lines = self.split_text_to_fit(entry, self.max_frame_width)
            for line in lines:
                if y_offset + self.entry_height > rect.bottom:
                    return
                pygame.draw.rect(self.screen, self.entry_background_color, pygame.Rect(
                    rect.x, y_offset, self.max_frame_width, self.entry_height))
                self.font.render_to(
                    self.screen, (rect.x + 5, y_offset + 5), line, self.text_color)
                y_offset += self.entry_height + 5

    def draw_adjustments(self, rect):
        pygame.draw.rect(self.screen, self.background_color, rect)
        y_offset = rect.y + 5

        if self.current_process_index < len(self.ajustes_list):
            desc = f"{self.ajustes_list[self.current_process_index]}"
            lines = self.split_text_to_fit(desc, self.max_frame_width)
            for line in lines:
                if y_offset + self.entry_height > rect.bottom:
                    return
                pygame.draw.rect(self.screen, self.entry_background_color, pygame.Rect(
                    rect.x, y_offset, self.max_frame_width, self.entry_height))
                self.font.render_to(
                    self.screen, (rect.x + 5, y_offset + 5), line, self.text_color)
                y_offset += self.entry_height + 5

    def split_text_to_fit(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_surface, _ = self.font.render(test_line, self.text_color)
            if test_surface.get_width() > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines

    def complete_current_process(self):
        if self.current_process_index < len(self.tratamientos_necesarios_list):
            self.add_to_history(f"[{time.strftime('%H:%M:%S')}] Proceso {
                                self.current_process_index + 1}: Culminado con éxito")

            self.current_process_index += 1
            if self.current_process_index < len(self.tratamientos_necesarios_list):
                self.add_to_history(f"[{time.strftime('%H:%M:%S')}] Proceso {
                                    self.current_process_index + 1}: Iniciado")
                self.start_time = time.time()
            else:
                self.processing = False
                self.add_post_process_description(
                    "Todos los procesos han sido completados.")

    def add_to_history(self, entry):
        if len(self.history) >= self.history_limit:
            self.history.pop(0)
        self.history.append(entry)

    def add_post_process_description(self, desc):
        self.post_process_descriptions.append(desc)
