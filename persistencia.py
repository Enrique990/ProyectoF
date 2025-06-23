import json
import os

DATOS_DIR = "datos"

def _ruta_archivo(nombre):
    return os.path.join(DATOS_DIR, nombre)

def guardar_json(nombre_archivo, datos):
    with open(_ruta_archivo(nombre_archivo), "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_json(nombre_archivo):
    ruta = f"datos/{nombre_archivo}" # Aseguramos que la ruta sea correcta
    if not os.path.exists(ruta):
        return []  # el archivo no existe todavía
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read().strip()
        if not contenido:
            return []  # archivo vacío → lista vacía
        return json.loads(contenido)

# Funciones específicas para cada archivo de datos
def guardar_equipo(equipos): guardar_json("equipo.json", equipos)
def cargar_equipo(): return cargar_json("equipo.json")

def guardar_roles(roles): guardar_json("roles.json", roles)
def cargar_roles(): return cargar_json("roles.json")

def guardar_tareas(tareas): guardar_json("tareas.json", tareas)
def cargar_tareas(): return cargar_json("tareas.json")