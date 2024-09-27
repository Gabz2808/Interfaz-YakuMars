import pygame
import time
from Data.processQueue import ProcessQueue
from Data.sampleData import ProcesosNecesarios, DataGenerator
from Utils.utils import Utils
import pygame.freetype


class ReporteFrame:
    def __init__(self, screen, rect, data):
        self.screen = screen
        self.rect = rect
        self.data = data

        # Inicializa Utils para colores y fuentes
        self.utils = Utils()

        self.history = []
        self.history_limit = 10
        self.current_process_index = 0
        self.processing = False

        # Inicializa los procesos necesarios
        self.procesos = {
            # Trampa de Grasa y Sedimentador
            "Pretratamiento": ["Turbidez", "ColiformesTotales"],
            # Tratamientos químicos
            "Electrocoagulación": ["Plomo", "Arsénico", "Mercurio", "ConcentraciónGas"],
            # Aireación
            "Aireación": ["pH", "OxígenoDisuelto", "Conductividad", "PresiónAtmosférica"],
            # Filtración por Membrana: Ultrafiltración
            "Ultrafiltración": ["VOC", "Uranio", "Radio", "Nitratos", "Nitritos", "PesticidasHerbicidas"],
            # Desinfección UV
            "Desinfección UV": ["ColiformesTotales", "E_coli", "IntensidadLumínica"],
            # Tratamiento ambiental
            # Por tratar:
            # ["Temperatura", "HumedadRelativa", , "PM10", "PM2_5"]
        }

        # Colores y fuentes
        self.background_color = self.utils.get_color("white")
        self.title_color = self.utils.get_color("black")
        self.text_color = self.utils.get_color("black")
        self.entry_background_color = self.utils.get_color("custom_color_1")
        self.max_frame_width = rect.width - 20
        self.max_frame_height = rect.height - 100
        self.entry_height = 20
        self.title_font = self.utils.get_font("title_font")


# Usar pygame.freetype para la fuente
        self.font = pygame.freetype.SysFont('Verdana', 14)

        # Tratamientos necesarios y ajustes
        self.tratamientos_necesarios_list = []
        self.ajustes_list = []

        # Instancias de generador de datos y procesos necesarios
        self.data_generator = DataGenerator()
        self.procesos_necesarios = ProcesosNecesarios()

        datos = self.data_generator.generar_datos_random()
        self.tratamientos_necesarios, self.ajustes, self.procesos_necesarios_list = self.procesos_necesarios.evaluar_tratamientos_necesarios(
            datos)

        # Procesos de purificación
        self.procesos_purificacion = [
            "Filtración de grasas y agua jabonosa", "Centrifugación", "Electrocoagulación",
            "Inyección de CO2", "Filtros de carbono activo", "Desinfección UV", "Balanceo"
        ]

        self.tratamientos_necesarios_list = [
            f"{param}: {'Sí' if necesita_tratamiento else 'No'}"
            for param, necesita_tratamiento in self.tratamientos_necesarios.items() if necesita_tratamiento
        ]

        # Cola de procesos
        self.process_queue = ProcessQueue()
        self.process_queue.queue = self.procesos_purificacion
        self.process_queue.total_steps = len(self.procesos_purificacion)
        self.process_queue.current_step = 0

        if self.tratamientos_necesarios_list:
            self.processing = True
            self.start_time = time.time()
            self.add_to_history(
                f"[{time.strftime('%H:%M:%S')}] Proceso 1: Iniciado")

        self.prepare_report_data()

    def prepare_report_data(self):
        ordered_processes = list(self.procesos.keys())
        self.tratamientos_necesarios_list = [
            f"{param}: {'Sí' if self.tratamientos_necesarios.get(
                param, False) else 'No'}"
            for param in ordered_processes
        ]
        self.ajustes_list = [
            f"{param}: Ajuste necesario de {ajuste:.2f}" for param, ajuste in self.ajustes.items() if ajuste is not None
        ]

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.rect)
        section_height = self.max_frame_height // 2

        # Sección para el historial
        history_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 50, self.max_frame_width, section_height - 25)

        # Sección para los ajustes (más arriba)
        adjustments_rect = pygame.Rect(
            self.rect.x + 10, self.rect.y + 50 + section_height - 25 + 5, self.max_frame_width, section_height)

        # Título del reporte de progreso
        title_surface = self.title_font.render(
            "Reporte de Progreso", True, self.title_color)
        self.screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 10))

        # Dibuja el historial
        self.draw_history(history_rect)

        # Título del reporte de ajustes
        adjustment_title_surface = self.title_font.render(
            "Reporte de Ajustes", True, self.title_color)
        self.screen.blit(adjustment_title_surface, (self.rect.x +
                                                    10, self.rect.y + 0 + section_height - 25 + 5))

        # Dibuja los ajustes
        self.draw_adjustments(adjustments_rect)

        # Procesamiento en progreso
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
                    break
                self.font.render_to(
                    self.screen, (rect.x + 5, y_offset), line, self.text_color)
                y_offset += self.entry_height

    def draw_adjustments(self, rect):
        pygame.draw.rect(self.screen, self.background_color, rect)
        y_offset = rect.y + 5

        for adjustment in self.ajustes_list:
            lines = self.split_text_to_fit(adjustment, self.max_frame_width)
            for line in lines:
                if y_offset + self.entry_height > rect.bottom:
                    break
                self.font.render_to(
                    self.screen, (rect.x + 5, y_offset), line, self.text_color)
                y_offset += self.entry_height

    def split_text_to_fit(self, text, max_width):
        lines = []
        words = text.split(" ")
        current_line = ""

        for word in words:
            # Usa `self.font.get_rect` para calcular el tamaño del texto con freetype
            text_rect = self.font.get_rect(current_line + " " + word)
            if text_rect.width <= max_width:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines

    def complete_current_process(self):
        self.current_process_index += 1

        if self.current_process_index >= len(self.tratamientos_necesarios_list):
            self.processing = False
            self.add_to_history(
                f"[{time.strftime('%H:%M:%S')}] Se ha completado el flujo")
        else:
            self.start_time = time.time()
            self.add_to_history(f"[{time.strftime('%H:%M:%S')}] Proceso {
                                self.current_process_index + 1}: Iniciado")

    def add_to_history(self, entry):
        self.history.append(entry)

        if len(self.history) > self.history_limit:
            self.history = self.history[-self.history_limit:]

    def get_current_process(self):
        if self.current_process_index < len(self.tratamientos_necesarios_list):
            return self.tratamientos_necesarios_list[self.current_process_index]
        return None
