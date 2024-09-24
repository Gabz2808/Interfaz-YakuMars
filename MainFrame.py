import sys
import pygame
from Frames.iconFrame import IconFrame
from Utils.utils import Utils
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
frame_height = 250
terminal_width = 300
terminal_height = 200
spacing = 20

# Ajustar posiciones para el layout solicitado
reporte_rect = pygame.Rect(screen_width - frame_width -
                           margin, margin, frame_width, screen_height - 2 * margin)
planta_rect = pygame.Rect(
    margin, margin, screen_width - frame_width - 2 * margin, frame_height)
progress_bar_rect = pygame.Rect(
    planta_rect.x + 15, planta_rect.bottom + 15, planta_rect.width - 30, 25)
terminal_rect = pygame.Rect(
    planta_rect.x, progress_bar_rect.bottom + 15, terminal_width, terminal_height)
planta_frame_rect = pygame.Rect(margin, margin, screen_width - frame_width - 2 * margin,
                                screen_height - (progress_bar_rect.height + terminal_height + 3 * spacing + 2 * margin))

# Crear los frames con los datos generados
reporte_frame = ReporteFrame(screen, reporte_rect, data)
planta_frame = PlantaFrame(screen, planta_frame_rect, data)
terminal_frame = TerminalFrame(
    screen, terminal_rect, reporte_frame, planta_frame)

# Evaluar los tratamientos necesarios
tratamientos_necesarios, ajustes, procesos_necesarios = procesos.evaluar_tratamientos_necesarios(
    data)

# Crear el IconFrame
icon_frame = IconFrame(screen, utils)

# Usar los colores de Utils
whiteColor = utils.get_color("white")

# Bucle principal para mantener la ventana abierta
running = True
alert_time = 0  # Tiempo para las alertas
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Manejar eventos de iconos
        icon_frame.handle_event(event)

    # Limpiar la pantalla
    screen.fill(whiteColor)

    # Actualizar los valores de los frames
    planta_frame.data_value = data.get(planta_frame.data_key, "N/A")
    terminal_frame.data_value = data.get(terminal_frame.data_key, "N/A")

    # Dibujar los frames actualizados
    reporte_frame.draw()
    planta_frame.draw()  # Se dibuja el frame con la imagen y el rectángulo centrado
    terminal_frame.draw()

    # Dibujar los íconos en el footer
    icon_frame.draw_icons()

    # Si han pasado 5 segundos (5000 ms), se cierra el mensaje
    if alert_time > 0 and pygame.time.get_ticks() - alert_time > 5000:
        alert_time = 0  # Reinicia el temporizador

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()
