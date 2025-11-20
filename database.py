import json
from datetime import datetime, timedelta
import os

# 📌 Directorio persistente permitido en Render FREE
BASE_DIR = "/opt/render/project/data"

# Crear directorio si no existe
os.makedirs(BASE_DIR, exist_ok=True)

# Archivo JSON permanente
DATA_FILE = os.path.join(BASE_DIR, "database.json")


def inicializar_bd():
    """Crea la base de datos si no existe dentro del almacenamiento persistente."""
    if not os.path.exists(DATA_FILE):
        data = {
            "usuarios_totales": 0,
            "historial_conexiones": [],
            "calificaciones": []
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Base de datos JSON creada en /opt/render/project/data/")


def leer_bd():
    inicializar_bd()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error leyendo BD: {e}")
        return {"usuarios_totales": 0, "historial_conexiones": [], "calificaciones": []}


def guardar_bd(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error guardando BD: {e}")
        return False


def obtener_hora_mexico():
    hora_utc = datetime.utcnow()
    return hora_utc - timedelta(hours=6)


def registrar_usuario():
    data = leer_bd()

    usuario_id = data["usuarios_totales"] + 1
    hora_mexico = obtener_hora_mexico()

    nueva_conexion = {
        "id": usuario_id,
        "fecha": hora_mexico.strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": hora_mexico.isoformat()
    }

    data["usuarios_totales"] = usuario_id
    data["historial_conexiones"].append(nueva_conexion)

    if guardar_bd(data):
        print(f"👤 Usuario #{usuario_id} registrado")
        return usuario_id

    return None


def obtener_usuarios_totales():
    data = leer_bd()
    return data["usuarios_totales"]


def obtener_historial():
    data = leer_bd()
    return data.get("historial_conexiones", [])


def guardar_calificacion(estrellas):
    if estrellas < 1 or estrellas > 5:
        return False

    data = leer_bd()
    hora_mexico = obtener_hora_mexico()

    nueva_calificacion = {
        "estrellas": estrellas,
        "fecha": hora_mexico.strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": hora_mexico.isoformat()
    }

    data["calificaciones"].append(nueva_calificacion)

    if guardar_bd(data):
        print(f"⭐ Calificación guardada: {estrellas} estrellas")
        return True

    return False


def cargar_calificaciones():
    data = leer_bd()
    calificaciones = data.get("calificaciones", [])

    total = len(calificaciones)
    promedio = round(sum(c["estrellas"] for c in calificaciones) / total, 1) if total > 0 else 0

    distribucion = {i: 0 for i in range(1, 6)}
    for c in calificaciones:
        distribucion[c["estrellas"]] += 1

    return {
        "promedio": promedio,
        "total_calificaciones": total,
        "distribucion": distribucion,
        "calificaciones": calificaciones
    }
    
