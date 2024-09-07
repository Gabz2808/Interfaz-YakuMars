import pygame
import sys


class ProcessDescriptionFrame:
    def __init__(self, tratamientosAsignados):
        self.width = 400  # Ajuste del ancho para mostrar más texto
        self.height = 250  # Ajuste de la altura
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))  # Fondo negro
        self.font = pygame.font.SysFont(None, 24)
        self.text = ["Descripción del proceso:"]

        # Agregar descripciones para cada tratamiento asignado
        for parametro, necesita_tratamiento in tratamientosAsignados.items():
            if necesita_tratamiento:
                self.text.append(self.generar_descripcion_proceso(parametro))

    def generar_descripcion_proceso(self, parametro):
        # Descripciones genéricas para cada tratamiento, puedes ajustar según sea necesario
        descripciones = {
            'Turbidez': "Reducción de turbidez mediante filtración.",
            'pH': "Ajuste del pH utilizando neutralizantes.",
            'ColiformesTotales': "Desinfección para eliminar coliformes totales.",
            'Conductividad': "Reducción de conductividad a través de ósmosis inversa.",
            'OxígenoDisuelto': "Aireación para ajustar los niveles de oxígeno disuelto.",
            'Plomo': "Eliminación de plomo mediante filtración de carbón activado.",
            'Arsénico': "Eliminación de arsénico usando filtros de adsorción.",
            'Mercurio': "Eliminación de mercurio mediante destilación.",
            'Nitratos': "Reducción de nitratos mediante biofiltración.",
            'Nitritos': "Eliminación de nitritos usando desionización.",
            'PesticidasHerbicidas': "Eliminación de pesticidas mediante filtración avanzada.",
            'VOC': "Reducción de compuestos orgánicos volátiles (VOC) por oxidación.",
            'Uranio': "Eliminación de uranio a través de procesos de intercambio iónico.",
            'Radio': "Reducción de radio mediante tratamiento químico.",
            'PM10': "Eliminación de partículas PM10 mediante filtros HEPA.",
            'PM2_5': "Eliminación de partículas PM2.5 mediante filtración electrostática.",
            'ConcentraciónGas': "Reducción de gases nocivos mediante ventilación y absorción."
        }
        # Si el parámetro tiene una descripción asociada, se usa. Si no, se pone un texto genérico.
        return descripciones.get(parametro, f"Aplicando tratamiento para {parametro}.")

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
        for i, line in enumerate(self.text):
            text_surface = self.font.render(
                line, True, (35, 213, 11))  # Texto verde
            screen.blit(text_surface, (x + 10, y + 10 + i * 25))
