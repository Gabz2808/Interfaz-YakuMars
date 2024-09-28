import pygame.freetype
from Frames.Frame import Frame


class TerminalFrame(Frame):
    def __init__(self, screen, rect, report_frame, planta_frame, title="Terminal de Ejecución"):
        super().__init__(screen, rect, title, "", "")
        self.report_frame = report_frame
        self.planta_frame = planta_frame  # Access to planta_frame for width
        self.font = pygame.freetype.SysFont('Verdana', 14)  # Font size
        self.title_font = pygame.freetype.SysFont(
            'Verdana', 18, bold=True)  # Title font size
        self.text_color = (0, 0, 0)  # Text color
        self.background_color = (240, 240, 240)  # Background color
        self.entry_height = 30  # Height of entry
        self.border_radius = 10  # Border radius for rounded rectangles

    def draw_rounded_rect(self, rect, color, radius):
        # Draw rounded rectangle using pygame's draw methods
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def draw_progress_bar(self):
        # Define the width of the progress bar to match the planta_frame width
        progress_bar_width = self.planta_frame.rect.width - 30  # Make the bar wider

        # Draw progress bar below the planta_frame
        progress_bar_rect = pygame.Rect(
            self.planta_frame.rect.x + 15, self.planta_frame.rect.bottom + 15, progress_bar_width, 25)
        pygame.draw.rect(self.screen, (200, 200, 200),
                         progress_bar_rect, border_radius=self.border_radius)

        current_index = self.report_frame.current_process_index
        total_processes = len(self.report_frame.tratamientos_necesarios_list)
        progress = int((current_index / total_processes)
                       * 100) if total_processes > 0 else 0

        # Draw progress bar fill
        progress_fill_rect = pygame.Rect(progress_bar_rect.x, progress_bar_rect.y, (
            progress_bar_width * (progress / 100)), progress_bar_rect.height)
        pygame.draw.rect(self.screen, (0, 150, 0),
                         progress_fill_rect, border_radius=self.border_radius)

        # Center the percentage text in the progress bar
        percentage_text = f"{progress}%"
        text_rect = self.font.get_rect(percentage_text)
        self.font.render_to(self.screen, (progress_bar_rect.x + (progress_bar_width - text_rect.width) / 2,
                            progress_bar_rect.y + (progress_bar_rect.height - text_rect.height) / 2), percentage_text, self.text_color)

    def draw(self):
        # Draw the frame background
        adjusted_rect = pygame.Rect(
            self.rect.x, self.planta_frame.rect.bottom + 50, self.rect.width, self.rect.height)
        self.screen.fill(self.background_color, adjusted_rect)

        # Draw the progress bar
        self.draw_progress_bar()

        # Actualiza la visibilidad de los rectángulos en PlantaFrame según el índice actual
        current_index = self.report_frame.current_process_index
        self.planta_frame.update_visibility(current_index)

        # Draw the frame title below the progress bar
        self.title_font.render_to(
            self.screen, (adjusted_rect.x + 15, adjusted_rect.y + 15), self.title, self.text_color)

        # Draw process status and description
        current_index = self.report_frame.current_process_index
        total_processes = len(self.report_frame.tratamientos_necesarios_list)

        # Inicia el proceso y establece el índice en 0 si es la primera ejecución
        if current_index == 0 and total_processes > 0:
            process_desc = "Proceso 1: Ejecutándose"
            description = self.report_frame.tratamientos_necesarios_list[0].split(":")[
                0]
        elif current_index < total_processes:
            process_desc = f"Proceso {current_index + 1}: Ejecutándose"
            description = self.report_frame.tratamientos_necesarios_list[current_index].split(":")[
                0]
        else:
            process_desc = "Todos los procesos completados"
            description = "No hay más procesos por ejecutar."

        # Display process description
        self.font.render_to(self.screen, (adjusted_rect.x + 15,
                            adjusted_rect.y + 50), process_desc, self.text_color)

        # Display brief description of the process
        description_y = adjusted_rect.y + 80
        self.font.render_to(self.screen, (adjusted_rect.x +
                            15, description_y), description, self.text_color)

    def draw_progress_bar(self):
        progress_bar_width = self.planta_frame.rect.width - 30
        progress_bar_rect = pygame.Rect(
            self.planta_frame.rect.x + 15, self.planta_frame.rect.bottom + 15, progress_bar_width, 25)
        pygame.draw.rect(self.screen, (200, 200, 200),
                         progress_bar_rect, border_radius=self.border_radius)

        current_index = self.report_frame.current_process_index
        total_processes = len(self.report_frame.tratamientos_necesarios_list)
        progress = int((current_index / total_processes)
                       * 100) if total_processes > 0 else 0

        # Dibujar el progreso
        progress_fill_rect = pygame.Rect(progress_bar_rect.x, progress_bar_rect.y,
                                         (progress_bar_width * (progress / 100)), progress_bar_rect.height)
        pygame.draw.rect(self.screen, (0, 150, 0),
                         progress_fill_rect, border_radius=self.border_radius)

        # Texto del porcentaje
        percentage_text = f"{progress}%"
        text_rect = self.font.get_rect(percentage_text)
        self.font.render_to(self.screen, (progress_bar_rect.x + (progress_bar_width - text_rect.width) / 2,
                            progress_bar_rect.y + (progress_bar_rect.height - text_rect.height) / 2), percentage_text, self.text_color)

        # Mantener visible el rectángulo celeste al 100%
        if progress == 100:
            # Asume que el rectángulo celeste es el índice 2
            self.planta_frame.rect_visibility[4] = True
            self.planta_frame.rect_visibility[3] = False

    def update_data(self, data):
        # Example logic to update some internal state or display based on new data
        self.current_data = data  # Storing data in an instance variable
        # Update any other necessary state or redraw the frame
