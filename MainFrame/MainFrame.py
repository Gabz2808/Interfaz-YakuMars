import sys
import pygame
from Frames.processFrame.processFrame import ProcessFrame, asignarTratamientos
from Frames.descriptionFrame.descriptionFrame import ProcessDescriptionFrame
from Frames.jsonFrame.jsonFrame import JsonResponseFrame
from Frames.progressBarFrame.progressBarFrame import ProgressBar
from Data.sampleData import DataGenerator
from anim.animations import Animations

# Inicializar Pygame
pygame.init()

# Cargar la imagen de las tuberías
image = pygame.image.load('tuberias.png')

# Instancia de la clase Animations
animations = Animations()

# Configurar la ventana
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# Dividir el ancho de la pantalla en 3 secciones iguales
section_width = screen_width // 3

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
progress_speed = 0.1
clock = pygame.time.Clock()

# Colores
black = (0, 0, 0)

# Variables de control para los textos de los marcos
terminal_text = "Procesos aplicados"
description_text = "Descripción del proceso"
json_response_text = "Datos generales"

# Variables de control para los estados de los textos
terminal_text_key = "terminal_text"
description_text_key = "description_text"
json_response_text_key = "json_response_text"

# Bucle principal para mantener la ventana abierta
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rellenar el fondo con color negro
    screen.fill(black)
    # Actualizar la barra de progreso
    progress_value += progress_speed
    if progress_value > 100:
        progress_value = 0
    progress_bar.update(progress_value)
    progress_bar.draw(screen)

    # Mostrar texto con efecto de escritura progresiva
    animations.type_writer_text(
        screen, "Bienvenido a YakuMars", (50, 50), key="welcome_text")
    screen.blit(image, (200, 100))

    # Aplicar el efecto de escritura progresiva para los textos de los marcos
    animations.type_writer_text(
        screen, json_response_text, (section_width // 2 - len(json_response_text) * 5 // 2, 300), key=json_response_text_key)
    animations.type_writer_text(
        screen, terminal_text, (section_width + section_width // 2 - len(terminal_text) * 5 // 2, 300), key=terminal_text_key)
    animations.type_writer_text(
        screen, description_text, (section_width * 2 + section_width // 2 - len(description_text) * 5 // 2, 300), key=description_text_key)

    # Aplicar la animación de desplazamiento
    animations.scroll_terminal_text(
        screen, json_response_frame, screen_height, 50)
    animations.scroll_terminal_text(screen, terminal_frame, screen_height, 450)
    animations.scroll_terminal_text(
        screen, description_frame, screen_height, 1000)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(30)

# Salir de Pygame
pygame.quit()
sys.exit()
