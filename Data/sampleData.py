import matplotlib.pyplot as plt
import numpy as np
import pygame
import io
import random


class DataGenerator:
    def __init__(self):
        pass

    def generar_datos_random(self):
        """Genera datos aleatorios para las muestras."""
        datos = {
            "Turbidez": round(random.uniform(0.0, 100.0), 2),  # NTU
            "pH": round(random.uniform(6.0, 9.0), 2),  # Sin unidad
            # UFC/100ml
            "ColiformesTotales": round(random.uniform(0.0, 1000.0), 2),
            "E_coli": round(random.uniform(0.0, 1000.0), 2),  # UFC/100ml
            "Conductividad": round(random.uniform(0.0, 2000.0), 2),  # µS/cm
            "OxígenoDisuelto": round(random.uniform(0.0, 14.0), 2),  # mg/L
            "Plomo": round(random.uniform(0.0, 0.05), 4),  # mg/L
            "Arsénico": round(random.uniform(0.0, 0.05), 4),  # mg/L
            "Mercurio": round(random.uniform(0.0, 0.006), 4),  # mg/L
            "Nitratos": round(random.uniform(0.0, 50.0), 2),  # mg/L
            "Nitritos": round(random.uniform(0.0, 10.0), 2),  # mg/L
            "PesticidasHerbicidas": round(random.uniform(0.0, 0.5), 2),  # mg/L
            "VOC": round(random.uniform(0.0, 0.5), 2),  # mg/L
            "Uranio": round(random.uniform(0.0, 30.0), 2),  # pCi/L
            "Radio": round(random.uniform(0.0, 5.0), 2),  # pCi/L
            "Temperatura": round(random.uniform(0.0, 40.0), 2),  # °C
            "HumedadRelativa": round(random.uniform(0.0, 100.0), 2),  # %
            # hPa
            "PresiónAtmosférica": round(random.uniform(900.0, 1100.0), 2),
            "PM10": round(random.uniform(0.0, 500.0), 2),  # µg/m³
            "PM2_5": round(random.uniform(0.0, 300.0), 2),  # µg/m³
            # lux
            "IntensidadLumínica": round(random.uniform(0.0, 10000.0), 2),
            "ConcentraciónGas": round(random.uniform(0.0, 1000.0), 2)  # ppm
        }
        return datos


class ProcesosNecesarios:
    def __init__(self, cantidad_agua_negras=500, cantidad_agua_grises=500):
        """Define los umbrales de calidad y cantidad de agua para los procesos."""
        self.cantidad_agua_negras = cantidad_agua_negras
        self.cantidad_agua_grises = cantidad_agua_grises
        self.total_agua_tratada = self.cantidad_agua_negras + self.cantidad_agua_grises

        self.umbrales = {
            "Turbidez": (0, 5.0),  # NTU después de la trampa de sólidos
            "pH": (6.5, 8.5),  # Rango aceptable de pH después de la aireación
            "ColiformesTotales": 0.0,  # Después de la desinfección UV
            "E_coli": 0.0,  # Después de la desinfección UV
            "Conductividad": 1500.0,  # Umbral de conductividad aceptable
            "OxígenoDisuelto": 5.0,  # Después de la aireación
            "Plomo": 0.01,  # Después de los tratamientos químicos
            "Arsénico": 0.01,
            "Mercurio": 0.002,
            "Nitratos": 10.0,
            "Nitritos": 1.0,
            "PesticidasHerbicidas": 0.1,
            "VOC": 0.1,
            "Uranio": 15.0,
            "Radio": 3.0,
            "Temperatura": (10.0, 30.0),  # Temperatura aceptable en procesos
            "HumedadRelativa": (30.0, 70.0),
            "PresiónAtmosférica": (950.0, 1050.0),
            "PM10": 50.0,
            "PM2_5": 25.0,
            "IntensidadLumínica": 500.0,
            "ConcentraciónGas": 100.0
        }

        self.procesos = {
            "Pretratamiento": ["Turbidez", "ColiformesTotales"],
            "Electrocoagulación": ["Plomo", "Arsénico", "Mercurio", "ConcentraciónGas"],
            "Aireación": ["pH", "OxígenoDisuelto", "Conductividad", "PresiónAtmosférica"],
            "Ultrafiltración": ["VOC", "Uranio", "Radio", "Nitratos", "Nitritos", "PesticidasHerbicidas"],
            "Desinfección UV": ["ColiformesTotales", "E_coli", "IntensidadLumínica"]
        }

    def evaluar_tratamientos_necesarios(self, datos):
        """Evalúa cada parámetro y determina si es necesario tratamiento y ajusta los datos."""
        tratamientos_asignados = {}
        ajustes = {}
        procesos_necesarios = []

        for parametro, valor in datos.items():
            if parametro in self.umbrales:
                umbral = self.umbrales[parametro]
                if isinstance(umbral, tuple):
                    if not (umbral[0] <= valor <= umbral[1]):
                        tratamientos_asignados[parametro] = True
                        ajustes[parametro] = umbral[0] if valor < umbral[0] else umbral[1]
                        procesos_necesarios += [proceso for proceso,
                                                params in self.procesos.items() if parametro in params]
                    else:
                        tratamientos_asignados[parametro] = False
                else:
                    if valor > umbral:
                        tratamientos_asignados[parametro] = True
                        ajustes[parametro] = umbral - valor
                        procesos_necesarios += [proceso for proceso,
                                                params in self.procesos.items() if parametro in params]
                    else:
                        tratamientos_asignados[parametro] = False
            else:
                tratamientos_asignados[parametro] = False

        # Retornar tratamientos asignados y los ajustes
        return tratamientos_asignados, ajustes, procesos_necesarios


class GraphicFrame:
    def __init__(self, ajustes):
        # Utilizamos los ajustes para generar el gráfico
        self.ajustes = ajustes

    def draw(self, screen):
        # Generar el gráfico y obtener la imagen
        pie_chart_surface = self.draw_pie_chart(self.ajustes)
        if pie_chart_surface:
            # Obtener el tamaño de la ventana de Pygame
            screen_rect = screen.get_rect()
            chart_rect = pie_chart_surface.get_rect(center=screen_rect.center)

            # Dibujar la imagen en el centro de la ventana de Pygame
            screen.blit(pie_chart_surface, chart_rect)

    def draw_pie_chart(self, ajustes):
        # Contar los ajustes para cada parámetro
        parametros = list(ajustes.keys())
        valores = list(ajustes.values())

        # Filtrar valores no negativos
        valores_no_negativos = [val for val in valores if val >= 0]
        parametros_no_negativos = [param for param,
                                   val in zip(parametros, valores) if val >= 0]

        # Comprobar si hay valores no negativos para mostrar
        if len(parametros_no_negativos) == 0:
            print("No hay ajustes que mostrar en el gráfico.")
            return None

        # Crear gráfico de pastel
        fig, ax = plt.subplots(figsize=(5, 5))  # Cambiado a tamaño más pequeño
        ax.pie(valores_no_negativos, labels=parametros_no_negativos, autopct='%1.1f%%',
               startangle=90, colors=plt.cm.Paired(np.arange(len(valores_no_negativos))))
        ax.axis('equal')  # Asegurar que el gráfico sea un círculo

        # Guardar gráfico en BytesIO para convertirlo a superficie de Pygame
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)  # Cerrar la figura para liberar memoria
        buf.seek(0)

        # Convertir la imagen a una superficie de Pygame
        pie_chart_surface = pygame.image.load(buf)
        return pie_chart_surface
