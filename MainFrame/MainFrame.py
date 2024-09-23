import sys
import pygame
import tkinter as tk
from tkinter import messagebox
from Utils.fonts import Utils
from Data.sampleData import DataGenerator, ProcesosNecesarios
from Frames.plantaFrame import PlantaFrame
from Frames.terminalFrame import TerminalFrame
from Frames.reportFrame import ReporteFrame

# Inicializar Pygame
pygame.init()

# Obtener la resolución del monitor
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Crear la instancia de Utils
utils = Utils()

# Crear instancias de DataGenerator y ProcesosNecesarios
data_generator = DataGenerator()
procesos = ProcesosNecesarios()

# Configurar la pantalla al tamaño completo del monitor
screen = pygame.display.set_mode((screen_width, screen_height))

# Obtener los datos generados
data = data_generator.generar_datos_random()

# Definir márgenes y espaciado entre los frames
margin = 20
frame_width = 400
frame_height = 250  # Altura del frame de planta
terminal_width = 300  # Ancho del frame de terminal reducido
terminal_height = 200  # Altura del frame de terminal reducida
spacing = 20

# Ajustar posiciones para el layout solicitado
reporte_rect = pygame.Rect(screen_width - frame_width - margin, margin, frame_width, screen_height - 2 * margin)
planta_rect = pygame.Rect(margin, margin, screen_width - frame_width - 2 * margin, frame_height)
progress_bar_rect = pygame.Rect(planta_rect.x + 15, planta_rect.bottom + 15, planta_rect.width - 30, 25)
terminal_rect = pygame.Rect(planta_rect.x, progress_bar_rect.bottom + 15, terminal_width, terminal_height)
planta_frame_rect = pygame.Rect(margin, margin, screen_width - frame_width - 2 * margin, screen_height - (progress_bar_rect.height + terminal_height + 3 * spacing + 2 * margin))

# Crear los frames con los datos generados
reporte_frame = ReporteFrame(screen, reporte_rect, data)
planta_frame = PlantaFrame(screen, planta_frame_rect, data)
terminal_frame = TerminalFrame(screen, terminal_rect, reporte_frame, planta_frame)

# Evaluar los tratamientos necesarios
tratamientos_necesarios, ajustes = procesos.evaluar_tratamientos_necesarios(data)

# Cargar las imágenes de los íconos
pause_icon = pygame.image.load('pause_icon.png')
reset_icon = pygame.image.load('reset_icon.png')
start_icon = pygame.image.load('start_icon.png')

# Escalar los íconos al tamaño deseado
icon_size = (50, 50)
pause_icon = pygame.transform.scale(pause_icon, icon_size)
reset_icon = pygame.transform.scale(reset_icon, icon_size)
start_icon = pygame.transform.scale(start_icon, icon_size)

# Definir las posiciones de los botones (ahora íconos)
button_width = 150
button_height = 50
button_spacing = 20

pause_button_rect = pygame.Rect((screen_width - 3 * button_width - 2 * button_spacing) // 2, screen_height - button_height - margin, button_width, button_height)
reset_button_rect = pygame.Rect(pause_button_rect.right + button_spacing, pause_button_rect.top, button_width, button_height)
start_button_rect = pygame.Rect(reset_button_rect.right + button_spacing, reset_button_rect.top, button_width, button_height)

# Colores definidos manualmente
whiteColor = (255, 255, 255)

# Variables para el estado de los botones
paused = False
started = False

# Función para dibujar un ícono en lugar de un botón
def draw_icon(screen, rect, icon):
    icon_rect = icon.get_rect(center=rect.center)
    screen.blit(icon, icon_rect)

# Función para mostrar ventanas emergentes con mensajes de alerta
def mostrar_ventana_alerta(message):
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    messagebox.showinfo("Alerta", message)
    root.destroy()  # Cerrar la ventana de Tkinter después de mostrar la alerta

# Bucle principal para mantener la ventana abierta
running = True
alert_time = 0  # Tiempo para las alertas
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
                alert_message = "Alerta: sistema pausado" if paused else "Alerta: sistema reanudado"
                mostrar_ventana_alerta(alert_message)
                alert_time = pygame.time.get_ticks()  # Marca el tiempo actual para controlar los 5 segundos
            elif reset_button_rect.collidepoint(event.pos):
                alert_message = "Alerta: sistema reiniciado"
                mostrar_ventana_alerta(alert_message)
                alert_time = pygame.time.get_ticks()
            elif start_button_rect.collidepoint(event.pos):
                started = True
                paused = False
                alert_message = "Alerta: sistema reanudado"
                mostrar_ventana_alerta(alert_message)
                alert_time = pygame.time.get_ticks()

    # Limpiar la pantalla
    screen.fill(whiteColor)

    # Actualizar los valores de los frames
    planta_frame.data_value = data.get(planta_frame.data_key, "N/A")
    terminal_frame.data_value = data.get(terminal_frame.data_key, "N/A")

    # Dibujar los frames actualizados
    reporte_frame.draw()
    planta_frame.draw()
    terminal_frame.draw()

    # Dibujar los íconos en el footer
    draw_icon(screen, pause_button_rect, pause_icon)
    draw_icon(screen, reset_button_rect, reset_icon)
    draw_icon(screen, start_button_rect, start_icon)

    # Si han pasado 5 segundos (5000 ms), se cierra el mensaje
    if alert_time > 0 and pygame.time.get_ticks() - alert_time > 5000:
        alert_time = 0  # Reinicia el temporizador

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
