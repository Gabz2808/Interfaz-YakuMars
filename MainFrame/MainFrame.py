'''
Esta clase inicia la venta principal de la interfaz gráfica, configurando el tamaño y los colores de la misma

'''
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana

info = pygame.display.Info()  # Obtiene información de la pantalla

screen_width = info.current_w  # Obtiene el ancho de la pantalla
screen_height = info.current_h  # Obtiene el alto de la pantalla

# Imprime el ancho y alto de la pantalla
print({screen_width}, {screen_height})
# Configura el tamaño de la ventana de la pantalla actual
screen = pygame.display.set_mode((screen_width, screen_height))
# Configura el nombre de la ventana
pygame.display.set_caption('Interfaz Gráfica YakuMars')

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Bucle principal para mantener la ventana abierta
running = True
while running:
    for event in pygame.event.get():  # Eventos de Pygame
        if event.type == pygame.QUIT:
            running = False

    # Rellenar el fondo
    screen.fill(white)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
