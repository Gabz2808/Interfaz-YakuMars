import pygame


class ProcessQueue:
    def __init__(self, process_duration=5):
        self.queue = []
        self.total_steps = 0
        self.current_step = 0
        self.processing = False
        self.process_duration = process_duration  # Duración en segundos
        self.current_process_time = 0  # Tiempo transcurrido para el proceso actual

    def start_processing(self):
        self.processing = True
        self.current_step = 0
        self.current_process_time = 0

    def update(self, delta_time):
        if not self.processing or self.current_step >= self.total_steps:
            return

        # Acumular el tiempo transcurrido
        self.current_process_time += delta_time

        # Si el proceso actual ha durado lo suficiente (5 segundos)
        if self.current_process_time >= self.process_duration:
            self.current_step += 1
            self.current_process_time = 0  # Reiniciar el tiempo para el próximo proceso

        # Si todos los procesos han terminado
        if self.current_step >= self.total_steps:
            self.processing = False
