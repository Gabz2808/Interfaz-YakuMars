import sys
import pygame
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
reporte_rect = pygame.Rect(screen_width - frame_width -
                           margin, margin, frame_width, screen_height - 2 * margin)

# La parte superior izquierda para planta_frame
planta_rect = pygame.Rect(
    margin, margin, screen_width - frame_width - 2 * margin, frame_height)

# Ajustar la posición de la barra de progreso para que esté justo debajo del planta_frame
progress_bar_rect = pygame.Rect(
    planta_rect.x + 15, planta_rect.bottom + 15, planta_rect.width - 30, 25)

# Ajustar la posición del terminal_frame para que esté en medio del reporte_frame y el resto del espacio
terminal_rect = pygame.Rect(
    planta_rect.x, progress_bar_rect.bottom + 15, terminal_width, terminal_height)

# Ajustar el tamaño del frame de planta para llenar el espacio restante
planta_frame_rect = pygame.Rect(margin, margin, screen_width - frame_width - 2 * margin,
                                screen_height - (progress_bar_rect.height + terminal_height + 3 * spacing + 2 * margin))

# Crear los frames con los datos generados
reporte_frame = ReporteFrame(screen, reporte_rect, data)
planta_frame = PlantaFrame(screen, planta_frame_rect, data)
terminal_frame = TerminalFrame(
    screen, terminal_rect, reporte_frame, planta_frame)  # Pasar planta_frame aquí

# Evaluar los tratamientos necesarios
tratamientos_necesarios, ajustes = procesos.evaluar_tratamientos_necesarios(
    data)

# Bucle principal para mantener la ventana abierta
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar la pantalla
    screen.fill(utils.whiteColor)

    # Actualizar los valores de los frames
    planta_frame.data_value = data.get(planta_frame.data_key, "N/A")
    terminal_frame.data_value = data.get(terminal_frame.data_key, "N/A")

    # Dibujar los frames actualizados
    reporte_frame.draw()
    planta_frame.draw()
    terminal_frame.draw()

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
