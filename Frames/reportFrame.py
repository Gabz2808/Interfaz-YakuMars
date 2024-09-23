import pygame
import pygame.freetype
from Data.processQueue import ProcessQueue
from Data.sampleData import ProcesosNecesarios, DataGenerator
import time
from Utils.utils import Utils


class ReporteFrame:
    def __init__(self, screen, rect, data):
        self.screen = screen
        self.rect = rect
        self.data = data

        # Inicializa la clase Utils para acceder a colores y fuentes
        self.utils = Utils()

        # Inicializa la historia y otros atributos necesarios
        self.history = []
        self.history_limit = 10
        self.current_process_index = 0
        self.processing = False

        # Inicializa los procesos necesarios
        self.procesos = {
            "Pretratamiento": ["Turbidez", "ColiformesTotales"],
            "Electrocoagulación": ["Plomo", "Arsénico", "Mercurio"],
            "Filtro Multicapa": ["Nitratos", "Nitritos", "PesticidasHerbicidas"],
            "Filtración por Membrana": ["VOC", "Uranio", "Radio"],
            "Desinfección UV": ["ColiformesTotales"]
        }

        # Inicializa atributos visuales
        self.background_color = self.utils.get_color("white")
        self.title_color = self.utils.get_color("black")
        self.text_color = self.utils.get_color("black")
        self.entry_background_color = self.utils.get_color("custom_color_1")
        self.max_frame_width = rect.width - 20
        self.max_frame_height = rect.height - 100
        self.entry_height = 20
        self.title_font = self.utils.get_font("title_font")
        self.font = self.utils.get_font("text_font")

        # Inicializa listas de tratamientos y ajustes
        self.tratamientos_necesarios_list = []
        self.ajustes_list = []

        # Crear instancias de generador de datos y procesos necesarios
        self.data_generator = DataGenerator()
        self.procesos_necesarios = ProcesosNecesarios()

        # Generar datos aleatorios
        datos = self.data_generator.generar_datos_random()

        # Evaluar tratamientos necesarios
        self.tratamientos_necesarios, self.ajustes, self.procesos_necesarios_list = self.procesos_necesarios.evaluar_tratamientos_necesarios(
            datos)

        # Lista de procesos en el orden requerido
        self.procesos_purificacion = [
            "Filtración de grasas y agua jabonosa",
            "Centrifugación",
            "Electrocoagulación",
            "Inyección de CO2",
            "Filtros de carbono activo",
            "Desinfección UV",
            "Balanceo (adición de cloro y otros químicos)"
        ]

        self.tratamientos_necesarios_list = [
            f"{param}: {'Sí' if necesita_tratamiento else 'No'}"
            for param, necesita_tratamiento in self.tratamientos_necesarios.items() if necesita_tratamiento
        ]

        # Asegúrate de que el orden de tratamientos sea respetado
        self.process_queue = ProcessQueue()
        self.process_queue.queue = self.procesos_purificacion
        self.process_queue.total_steps = len(self.procesos_purificacion)
        self.process_queue.current_step = 0

        if self.tratamientos_necesarios_list:
            self.processing = True
            self.start_time = time.time()
            self.add_to_history(
                f"[{time.strftime('%H:%M:%S')}] Proceso 1: Iniciado")

        # Prepara los datos del reporte
        self.prepare_report_data()

    def prepare_report_data(self):
        ordered_processes = list(self.procesos.keys())
        self.tratamientos_necesarios_list = [
            f"{param}: {'Sí' if self.tratamientos_necesarios.get(
                param, False) else 'No'}"
            for param in ordered_processes
        ]

        self.ajustes_list = [
            f"{param}: Ajuste necesario de {ajuste:.2f}"
            for param, ajuste in self.ajustes.items() if ajuste is not None
        ]

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.rect)

        # Ajustar altura para dividir el espacio
        section_height = self.max_frame_height // 2
        history_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 50, self.max_frame_width, section_height
        )

        # Colocar el panel de ajustes directamente debajo del historial
        adjustments_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 50 + section_height +
            5, self.max_frame_width, section_height
        )

        # Renderizar el título
        title_surface = self.title_font.render(
            "Reporte de Progreso", True, self.title_color)
        self.screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 10))

        self.draw_history(history_rect)
        self.draw_adjustments(adjustments_rect)

        if self.processing:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 2:
                self.complete_current_process()

    def draw_history(self, rect):
        pygame.draw.rect(self.screen, self.background_color, rect)
        y_offset = rect.y + 5

        for entry in self.history[-self.history_limit:]:
            lines = self.split_text_to_fit(entry, self.max_frame_width)
            for line in lines:
                if y_offset + self.entry_height > rect.bottom:
                    return
                pygame.draw.rect(self.screen, self.entry_background_color, pygame.Rect(
                    rect.x, y_offset, self.max_frame_width, self.entry_height))
                text_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(text_surface, (rect.x + 5, y_offset + 5))
                y_offset += self.entry_height + 5

    def draw_adjustments(self, rect):
        pygame.draw.rect(self.screen, self.background_color, rect)
        y_offset = rect.y + 5

        # Renderizar el título
        title_surface = self.title_font.render(
            "Reporte de Ajustes", True, self.title_color)
        self.screen.blit(title_surface, (rect.x + 5, y_offset))
        y_offset += self.entry_height + 15  # Espacio debajo del título

        # Recorre todos los procesos
        for parametros in self.procesos.values():
            # Recorre todos los parámetros asociados a ese proceso
            for param in parametros:
                # Comprueba si se necesita ajuste para ese parámetro
                ajuste = self.ajustes.get(param, None)
                if ajuste is not None:
                    # Agregar "+" para los ajustes no negativos
                    ajuste_text = f"{param}: {
                        '+' if ajuste >= 0 else ''}{ajuste:.2f}"

                    # Renderiza la información de ajuste
                    lines = self.split_text_to_fit(
                        ajuste_text, self.max_frame_width)
                    for line in lines:
                        if y_offset + self.entry_height > rect.bottom:
                            return  # Si el texto se sale del cuadro, salimos
                        pygame.draw.rect(self.screen, self.entry_background_color, pygame.Rect(
                            rect.x, y_offset, self.max_frame_width, self.entry_height))
                        text_surface = self.font.render(
                            line, True, self.text_color)
                        self.screen.blit(
                            text_surface, (rect.x + 5, y_offset + 5))
                        y_offset += self.entry_height + 5

    def split_text_to_fit(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_surface = self.font.render(test_line, True, self.text_color)
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
        if not hasattr(self, 'post_process_descriptions'):
            self.post_process_descriptions = []
        self.post_process_descriptions.append(desc)
