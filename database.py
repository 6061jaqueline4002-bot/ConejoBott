import json
import os
from datetime import datetime

DATA_FILE = "database.json"

def inicializar_bd():
    """Inicializa la base de datos JSON si no existe"""
    if not os.path.exists(DATA_FILE):
        data = {
            "usuarios_totales": 0,
            "historial_conexiones": [],
            "calificaciones": []
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Base de datos JSON inicializada")

def leer_bd():
    """Lee toda la base de datos"""
    inicializar_bd()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error leyendo BD: {e}")
        return {"usuarios_totales": 0, "historial_conexiones": [], "calificaciones": []}

def guardar_bd(data):
    """Guarda toda la base de datos"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error guardando BD: {e}")
        return False

def registrar_usuario():
    """Registra un nuevo usuario en el historial"""
    data = leer_bd()
    usuario_id = data["usuarios_totales"] + 1
    
    nueva_conexion = {
        "id": usuario_id,
        "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": datetime.now().isoformat()
    }
    
    data["usuarios_totales"] = usuario_id
    data["historial_conexiones"].append(nueva_conexion)
    
    if guardar_bd(data):
        print(f"✅ Usuario #{usuario_id} registrado")
        return usuario_id
    return None

def obtener_usuarios_totales():
    """Obtiene el total de usuarios registrados"""
    data = leer_bd()
    return data["usuarios_totales"]

def obtener_historial():
    """Obtiene el historial completo de conexiones"""
    data = leer_bd()
    return data.get("historial_conexiones", [])

def guardar_calificacion(estrellas, comentario=""):
    """Guarda una nueva calificación"""
    if estrellas < 1 or estrellas > 5:
        return False
        
    data = leer_bd()
    
    nueva_calificacion = {
        "estrellas": estrellas,
        "comentario": comentario,
        "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": datetime.now().isoformat()
    }
    
    data["calificaciones"].append(nueva_calificacion)
    
    if guardar_bd(data):
        print(f"✅ Calificación {estrellas}⭐ guardada")
        return True
    return False

def cargar_calificaciones():
    """Carga todas las calificaciones con estadísticas"""
    data = leer_bd()
    calificaciones = data.get("calificaciones", [])
    total = len(calificaciones)
    
    # Calcular promedio
    promedio = 0
    if total > 0:
        suma = sum(c["estrellas"] for c in calificaciones)
        promedio = round(suma / total, 1)
    
    # Calcular distribución
    distribucion = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for calif in calificaciones:
        estrellas = calif["estrellas"]
        if 1 <= estrellas <= 5:
            distribucion[estrellas] += 1
    
    return {
        "promedio": promedio,
        "total_calificaciones": total,
        "distribucion": distribucion,
        "calificaciones": calificaciones
    }
