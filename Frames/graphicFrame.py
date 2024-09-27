import matplotlib.pyplot as plt
import numpy as np
import pygame
import io


class GraphicFrame:
    def __init__(self, procesos_necesarios):
        # Utilizamos los procesos necesarios para generar el gráfico
        self.procesos_necesarios = procesos_necesarios

    def draw(self, screen):
        # Generar el gráfico y obtener la imagen
        pie_chart_surface = self.draw_pie_chart(self.procesos_necesarios)
        if pie_chart_surface:
            # Obtener el tamaño de la ventana de Pygame
            screen_rect = screen.get_rect()

            # Redimensionar el gráfico a un tamaño intermedio
            pie_chart_surface = pygame.transform.scale(
                pie_chart_surface, (300, 300))

            # Desplazar el gráfico hacia abajo sumando un offset al midtop
            chart_rect = pie_chart_surface.get_rect(
                midtop=(screen_rect.centerx, screen_rect.centery + 100))

            # Dibujar la imagen en la posición especificada
            screen.blit(pie_chart_surface, chart_rect)

    def draw_pie_chart(self, procesos_necesarios):
        # Contar los procesos necesarios y sus ocurrencias
        conteo_procesos = {proceso: 0 for proceso in procesos_necesarios}
        for proceso in procesos_necesarios:
            conteo_procesos[proceso] += 1

        # Obtener parámetros y valores para el gráfico
        parametros = list(conteo_procesos.keys())
        valores = list(conteo_procesos.values())

        # Filtrar valores no negativos
        valores_no_negativos = [val for val in valores if val > 0]
        parametros_no_negativos = [param for param,
                                   val in zip(parametros, valores) if val > 0]

        # Comprobar si hay valores no negativos para mostrar
        if len(parametros_no_negativos) == 0:
            print("No hay procesos que mostrar en el gráfico.")
            return None

        # Crear gráfico de pastel con un tamaño intermedio
        fig, ax = plt.subplots(figsize=(6, 6))  # Tamaño intermedio del gráfico
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
