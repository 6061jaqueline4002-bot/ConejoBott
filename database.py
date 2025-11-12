import json
import os
from datetime import datetime, timedelta  # ← Asegúrate de importar timedelta

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

def obtener_hora_mexico():
    """Obtiene la hora actual en zona horaria de México (UTC-6)"""
    hora_utc = datetime.utcnow()
    # Ajustar a horario de México Central (UTC-6)
    hora_mexico = hora_utc - timedelta(hours=6)  # ← Ahora timedelta está importado
    return hora_mexico

def registrar_usuario():
    """Registra un nuevo usuario en el historial con hora local de México"""
    data = leer_bd()
    usuario_id = data["usuarios_totales"] + 1
    
    # Obtener hora local de México
    hora_mexico = obtener_hora_mexico()
    
    nueva_conexion = {
        "id": usuario_id,
        "fecha": hora_mexico.strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": hora_mexico.isoformat()
    }
    
    data["usuarios_totales"] = usuario_id
    data["historial_conexiones"].append(nueva_conexion)
    
    if guardar_bd(data):
        print(f"✅ Usuario #{usuario_id} registrado a las {hora_mexico.strftime('%H:%M:%S')}")
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

def guardar_calificacion(estrellas):
    """Guarda una nueva calificación con hora local de México"""
    if estrellas < 1 or estrellas > 5:
        return False
        
    data = leer_bd()
    
    # Obtener hora local de México
    hora_mexico = obtener_hora_mexico()
    
    nueva_calificacion = {
        "estrellas": estrellas,
        "fecha": hora_mexico.strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": hora_mexico.isoformat()
    }
    
    data["calificaciones"].append(nueva_calificacion)
    
    if guardar_bd(data):
        print(f"✅ Calificación {estrellas}⭐ guardada a las {hora_mexico.strftime('%H:%M:%S')}")
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
