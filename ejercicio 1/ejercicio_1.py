import re

def limpiar_registro_sensor(registro_raw):
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()
    temp_raw = str(registro_raw.get("temperatura", "0"))
    match = re.search(r"[-+]?\d*\.\d+|\d+", temp_raw)
    temperatura = float(match.group()) if match else 0.0
    ubicacion = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion).strip() if ubicacion and str(ubicacion).strip() else "Planta Principal"
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }

def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    if not lista_sensores_limpios:
        return [], 0.0
    sensores_alerta = [s["sensor_id"] for s in lista_sensores_limpios if s["temperatura"] > umbral_temperatura]
    promedio_temperatura = sum(s["temperatura"] for s in lista_sensores_limpios) / len(lista_sensores_limpios)
    return sensores_alerta, promedio_temperatura

# Bloque de ejecución y pruebas
if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.2 °C ", "ubicacion": ""},
        {"sensor_id": " SENSOR-003 ", "temperatura": "19.8 C", "ubicacion": "Planta Sur"}
    ]
    
    limpios = [limpiar_registro_sensor(r) for r in registros_crudos]
    alertas, promedio = generar_resumen_sensores(limpios, 25.0)
    
    print("--- REPORTE DE SENSORES ---")
    print(f"Registros limpios: {limpios}")
    print(f"Sensores en alerta (> 25°C): {alertas}")
    print(f"Promedio de temperatura: {promedio:.2f} °C")