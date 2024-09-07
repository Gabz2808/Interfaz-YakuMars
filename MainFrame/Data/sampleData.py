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
