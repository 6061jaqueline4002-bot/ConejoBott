import json, os
from datetime import datetime

DATA_FILE = "database.json"

def inicializar_bd():
    if not os.path.exists(DATA_FILE):
        data = {
            "usuarios_totales": 0,
            "historial": [],
            "calificaciones": []
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def leer_bd():
    inicializar_bd()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_bd(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def registrar_usuario():
    data = leer_bd()
    data["usuarios_totales"] += 1
    data["historial"].append(f"Usuario #{data['usuarios_totales']} - Conexión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    guardar_bd(data)

def obtener_usuarios():
    data = leer_bd()
    return data["usuarios_totales"]

def guardar_calificacion(estrellas):
    data = leer_bd()
    data["calificaciones"].append({
        "estrellas": estrellas,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    guardar_bd(data)
    return True

def cargar_calificaciones():
    data = leer_bd()
    califs = data.get("calificaciones", [])
    total = len(califs)
    promedio = round(sum(c["estrellas"] for c in califs) / total, 1) if total > 0 else 0

    distribucion = {str(i): 0 for i in range(1, 6)}
    for c in califs:
        distribucion[str(c["estrellas"])] += 1

    return {
        "promedio": promedio,
        "total_calificaciones": total,
        "distribucion": distribucion,
        "calificaciones": califs
    }

def obtener_historial():
    data = leer_bd()
    return data.get("historial", [])
