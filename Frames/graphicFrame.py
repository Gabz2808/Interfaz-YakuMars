import pygame
import math
from Frames.Frame import Frame


class GraficoAguaFrame(Frame):
    def __init__(self, screen, rect, data):
        title = "Gráfico de Agua Tratada"
        data_key = "OxígenoDisuelto"
        super().__init__(screen, rect, title, data_key, data.get(data_key, 0))
        self.data_values = []  # Para almacenar los datos de agua tratada

    def update_data(self, new_data):
        # Actualizar los datos del gráfico
        self.data_values.append(new_data)
        # Actualiza self.data con el nuevo valor
        self.data[self.data_key] = new_data
        if len(self.data_values) > 10:  # Limitar la cantidad de datos para el gráfico
            self.data_values.pop(0)

    def draw(self):
        # Dibujar el fondo del marco
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

        # Dibujar el marco
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect,
                         2)  # Marco de 2 píxeles de grosor

        # Dibujar el título del marco
        title_surface = self.font.render(self.title, True, (0, 0, 0))
        self.screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 10))

        # Dibujar el gráfico circular
        if self.data_values:
            total = sum(self.data_values)
            if total > 0:  # Para evitar división por cero
                start_angle = 0
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                          (255, 255, 0), (0, 255, 255)]

                for i, value in enumerate(self.data_values):
                    angle = (value / total) * 360
                    end_angle = start_angle + angle

                    # Dibujar el segmento del gráfico
                    pygame.draw.arc(
                        self.screen,
                        colors[i % len(colors)],
                        (self.rect.x + 10, self.rect.y + 40,
                         self.rect.width - 20, self.rect.height - 50),
                        math.radians(start_angle),
                        math.radians(end_angle),
                        0
                    )

                    # Dibuja una línea desde el centro al borde del gráfico
                    center_x = self.rect.x + self.rect.width // 2
                    center_y = self.rect.y + self.rect.height // 2 + 20  # Ajustar para el título
                    end_x = center_x + (self.rect.width // 2 - 10) * \
                        math.cos(math.radians((start_angle + end_angle) / 2))
                    end_y = center_y + (self.rect.height // 2 - 10) * \
                        math.sin(math.radians((start_angle + end_angle) / 2))
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (center_x, center_y + 20), (end_x, end_y), 2)

                    start_angle = end_angle

        # Dibujar los datos actuales
        current_value = self.data.get(self.data_key, 0)  # Cambia "N/A" a 0
        data_surface = self.font.render(
            f"Oxígeno Disuelto: {current_value}", True, (0, 0, 0))
        self.screen.blit(data_surface, (self.rect.x + 10,
                                        self.rect.y + self.rect.height - 30))
