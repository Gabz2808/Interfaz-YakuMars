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
    def __init__(self):
        """Define los umbrales de calidad para cada parámetro."""
        self.umbrales = {
            "Turbidez": 5.0,  # NTU
            "pH": (6.5, 8.5),  # Rango aceptable de pH
            "ColiformesTotales": 0.0,  # Cualquier valor > 0 requiere tratamiento
            "Conductividad": 1000.0,  # µS/cm
            "OxígenoDisuelto": 5.0,  # mg/L mínimo
            "Plomo": 0.01,  # mg/L máximo permitido
            "Arsénico": 0.01,  # mg/L máximo permitido
            "Mercurio": 0.002,  # mg/L máximo permitido
            "Nitratos": 10.0,  # mg/L máximo permitido
            "Nitritos": 1.0,  # mg/L máximo permitido
            "PesticidasHerbicidas": 0.1,  # mg/L máximo permitido
            "VOC": 0.1,  # mg/L máximo permitido
            "Uranio": 15.0,  # pCi/L máximo permitido
            "Radio": 3.0,  # pCi/L máximo permitido
            "PM10": 50.0,  # µg/m³ máximo permitido
            "PM2_5": 25.0,  # µg/m³ máximo permitido
            "ConcentraciónGas": 100.0  # ppm máximo permitido
        }

    def evaluar_tratamientos_necesarios(self, datos):
        """Evalúa cada parámetro y determina si es necesario tratamiento y ajusta los datos."""
        tratamientos_asignados = {}
        ajustes = {}
        for parametro, valor in datos.items():
            if parametro in self.umbrales:
                umbral = self.umbrales[parametro]
                if isinstance(umbral, tuple):
                    # Para rangos como el pH
                    if not (umbral[0] <= valor <= umbral[1]):
                        tratamientos_asignados[parametro] = True
                        ajustes[parametro] = umbral[0] if valor < umbral[0] else umbral[1]
                    else:
                        tratamientos_asignados[parametro] = False
                else:
                    # Para parámetros con valor máximo
                    if valor > umbral:
                        tratamientos_asignados[parametro] = True
                        ajustes[parametro] = umbral - valor
                    else:
                        tratamientos_asignados[parametro] = False
            else:
                # Si no hay un umbral definido, no se requiere tratamiento
                tratamientos_asignados[parametro] = False
        return tratamientos_asignados, ajustes


# Ejemplo de uso
if __name__ == "__main__":
    procesos = ProcesosNecesarios()
    data_generator = DataGenerator()
    data = data_generator.generar_datos_random()

    # Evaluar los tratamientos necesarios y ajustes
    tratamientos_necesarios, ajustes, descripciones = procesos.evaluar_tratamientos_necesarios(
        data)

    # Obtener las claves de tratamientos necesarios
    process_keys = list(tratamientos_necesarios.keys())

    print("Tratamientos necesarios:")
    for key in process_keys:
        print(f"{key}: {'Sí' if tratamientos_necesarios[key] else 'No'}")

    print("\nAjustes:")
    for key, ajuste in ajustes.items():
        print(f"{key}: Ajuste necesario de {ajuste:.2f}")

    print("\nDescripciones:")
    for key, descripcion in descripciones.items():
        print(f"{key}: {descripcion}")
