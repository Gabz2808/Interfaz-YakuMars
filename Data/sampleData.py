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
        """Define los umbrales de calidad para cada parámetro en relación con los procesos de tratamiento."""
        self.umbrales = {
            "Turbidez": (0, 5.0),  # NTU después de la trampa de sólidos
            "pH": (6.5, 8.5),  # Rango aceptable de pH después de la aireación
            "ColiformesTotales": 0.0,  # Después de la desinsectación UV
            "OxígenoDisuelto": 5.0,  # Después de la aireación
            "Plomo": 0.01,  # Después de los tratamientos químicos
            "Arsénico": 0.01,
            "Mercurio": 0.002,
            "Nitratos": 10.0,
            "Nitritos": 1.0,
            "PesticidasHerbicidas": 0.1,
            "VOC": 0.1,
            "Uranio": 15.0,
            "Radio": 3.0,
            "ConcentraciónGas": 100.0  # Control de gases en el proceso
        }

        self.procesos = {
            # Trampa de Grasa y Sedimentador
            "Pretratamiento": ["Turbidez", "ColiformesTotales"],
            # Tratamientos químicos
            "Electrocoagulación": ["Plomo", "Arsénico", "Mercurio"],
            # Filtración de contaminantes
            "Filtro Multicapa": ["Nitratos", "Nitritos", "PesticidasHerbicidas"],
            # Filtración avanzada
            "Filtración por Membrana": ["VOC", "Uranio", "Radio"],
            "Desinfección UV": ["ColiformesTotales"]  # Desinfección final
        }

    def evaluar_tratamientos_necesarios(self, datos):
        """Evalúa cada parámetro y determina si es necesario tratamiento y ajusta los datos."""
        tratamientos_asignados = {}
        ajustes = {}
        procesos_necesarios = []

        for parametro, valor in datos.items():
            if parametro in self.umbrales:
                umbral = self.umbrales[parametro]
                if isinstance(umbral, tuple):
                    # Para rangos como el pH y Turbidez
                    if not (umbral[0] <= valor <= umbral[1]):
                        tratamientos_asignados[parametro] = True
                        ajustes[parametro] = umbral[0] if valor < umbral[0] else umbral[1]
                        procesos_necesarios += [proceso for proceso,
                                                params in self.procesos.items() if parametro in params]
                    else:
                        tratamientos_asignados[parametro] = False
                else:
                    # Para parámetros con valor máximo
                    if valor > umbral:
                        tratamientos_asignados[parametro] = True
                        ajustes[parametro] = umbral - valor
                        procesos_necesarios += [proceso for proceso,
                                                params in self.procesos.items() if parametro in params]
                    else:
                        tratamientos_asignados[parametro] = False
            else:
                tratamientos_asignados[parametro] = False

        return tratamientos_asignados, ajustes, procesos_necesarios
