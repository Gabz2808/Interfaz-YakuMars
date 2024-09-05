import sys
import pygame
from Frames.processFrame.processFrame import ProcessFrame
from Frames.descriptionFrame.descriptionFrame import ProcessDescriptionFrame
from Frames.jsonFrame.jsonFrame import JsonResponseFrame
from Frames.progressBarFrame.progressBarFrame import ProgressBar
# Inicializar Pygame
pygame.init()

# Configurar la ventana

info = pygame.display.Info()  # Obtiene información de la pantalla
screen_width = info.current_w  # Ancho de la pantalla
screen_height = info.current_h  # Alto de la pantalla

# Imprimir el ancho y alto de la pantalla
print(f"Ancho de pantalla: {screen_width}, Alto de pantalla: {screen_height}")

# Configurar el tamaño de la ventana para que ocupe toda la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))

# Crear una instancia de las demás clases
progress_bar = ProgressBar(0, screen_height // 2 - 20, screen_width, 40)
terminal_frame = ProcessFrame()
description_frame = ProcessDescriptionFrame()
json_response_frame = JsonResponseFrame()
# Configurar el nombre de la ventana
pygame.display.set_caption('Interfaz Gráfica YakuMars')

# Variables para controlar el progreso de la barra de progreso
progress_value = 0
progress_speed = 0.1  # Velocidad de incremento del progreso
clock = pygame.time.Clock()

# Colores
black = (0, 0, 0)

# Bucle principal para mantener la ventana abierta
running = True
while running:
    for event in pygame.event.get():  # Manejo de eventos de Pygame
        if event.type == pygame.QUIT:  # Evento de cerrar la ventana
            running = False

    # Rellenar el fondo con color blanco
    screen.fill(black)

    # Dibujar todos los frames en la pantalla
    # Draw the frames on the screen
    terminal_frame.draw(screen, 50, 500)
    description_frame.draw(screen, 450, 500)
    json_response_frame.draw(screen, 750, 500)

    # Actualizar el progreso (incrementa cada fotograma)
    progress_value += progress_speed
    if progress_value > 100:
        progress_value = 0  # Reinicia la barra cuando llegue al 100%

        # Actualizar y dibujar la barra de progreso
    progress_bar.update(progress_value)
    progress_bar.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60)  # Limitar a 60 FPS

# Salir de Pygame
pygame.quit()
sys.exit()
