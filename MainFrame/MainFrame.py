import sys
import pygame
from Frames.processFrame.processFrame import ProcessFrame, asignarTratamientos
from Frames.descriptionFrame.descriptionFrame import ProcessDescriptionFrame
from Frames.jsonFrame.jsonFrame import JsonResponseFrame
from Frames.progressBarFrame.progressBarFrame import ProgressBar
from Data.sampleData import DataGenerator

# Inicializar Pygame
pygame.init()
# Cargar la imagen de las tuberías
# image = pygame.image.load("tuberias.jpg")
# Configurar la ventana
info = pygame.display.Info()  # Obtiene información de la pantalla
screen_width = info.current_w  # Ancho de la pantalla
screen_height = info.current_h  # Alto de la pantalla

# Configurar el tamaño de la ventana para que ocupe toda la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))

# Generar datos randoms
data_generator = DataGenerator()
datos_muestra = data_generator.generar_datos_random()

# Procesar los tratamientos
tratamientosAsignados = asignarTratamientos(datos_muestra)

# Crear una instancia de las demás clases
progress_bar = ProgressBar(0, screen_height // 2 - 20, screen_width, 40)
terminal_frame = ProcessFrame()
description_frame = ProcessDescriptionFrame(tratamientosAsignados)
json_response_frame = JsonResponseFrame(datos_muestra)

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

    # Rellenar el fondo con color negro
    screen.fill(black)
   # screen.blit(image, (50, 50))  # Posicionar la imagen en (50, 50)

    # Dibujar todos los frames en la pantalla
    terminal_frame.draw(screen, 50, 500)
    description_frame.draw(screen, 450, 500)
    json_response_frame.draw(screen, 1000, 500)

    progress_bar.draw(screen)

    # Actualizar la barra de progreso
    progress_value += progress_speed
    if progress_value > 100:
        progress_value = 0
    progress_bar.update(progress_value)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(30)  # FPS

# Salir de Pygame
pygame.quit()
sys.exit()
