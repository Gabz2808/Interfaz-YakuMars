import pygame
import sys
from Data.sampleData import DataGenerator

# Definir los límites para cada parámetro
limites = {
    'Turbidez': {'min': 0.0, 'max': 5.0},
    'pH': {'min': 6.5, 'max': 8.5},
    'ColiformesTotales': {'min': 0, 'max': 0.0},
    'Conductividad': {'min': 0.0, 'max': 500.0},
    'OxígenoDisuelto': {'min': 5.0, 'max': 10.0},
    'Plomo': {'min': 0.0, 'max': 0.015},
    'Arsénico': {'min': 0.0, 'max': 0.01},
    'Mercurio': {'min': 0.0, 'max': 0.002},
    'Nitratos': {'min': 0.0, 'max': 10.0},
    'Nitritos': {'min': 0.0, 'max': 1.0},
    'PesticidasHerbicidas': {'min': 0.0, 'max': 0.1},
    'VOC': {'min': 0.0, 'max': 0.1},
    'Uranio': {'min': 0.0, 'max': 30.0},
    'Radio': {'min': 0.0, 'max': 5.0},
    'PM10': {'min': 0.0, 'max': 150.0},
    'PM2_5': {'min': 0.0, 'max': 35.0},
    'ConcentraciónGas': {'min': 0.0, 'max': 500.0},
}

# Crear una instancia de DataGenerator
data_generator = DataGenerator()

# Generar datos aleatorios
datos_muestra = data_generator.generar_datos_random()

# Procesar los tratamientos


def asignarTratamientos(datos):
    tratamientos = {}
    for parametro, valor in datos.items():
        if isinstance(valor, dict):
            for subParametro, subValor in valor.items():
                if subValor > limites[parametro][subParametro]['max']:
                    tratamientos[subParametro] = True
                else:
                    tratamientos[subParametro] = False
        else:
            if parametro in limites:
                if valor < limites[parametro]['min'] or valor > limites[parametro]['max']:
                    tratamientos[parametro] = True
                else:
                    tratamientos[parametro] = False
    return tratamientos


# Resultados de tratamientos usando los datos generados
tratamientosAsignados = asignarTratamientos(datos_muestra)


class ProcessFrame:
    def __init__(self):
        self.width = 250
        self.height = 150
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))  # Fondo negro
        self.font = pygame.font.SysFont(None, 24)
        self.tratamientosAsignados = tratamientosAsignados
        self.text = ["Tratamientos asignados:"]
        for key, value in self.tratamientosAsignados.items():
            self.text.append(f"{key}: {value}")

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
        for i, line in enumerate(self.text):
            text_surface = self.font.render(
                line, True, (35, 213, 11))  # Texto verde
            screen.blit(text_surface, (x + 10, y + 10 + i * 25))
