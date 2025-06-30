import json, os
from collections import defaultdict

archivo_tareas = "datos/tareas.json"
tareas = []

def cargar_datos_tareas():
    global tareas
    if os.path.exists(archivo_tareas):
        with open(archivo_tareas, "r", encoding="utf-8") as f:
            tareas = json.load(f)
    else:
        tareas = []

def guardar_datos_tareas():
    os.makedirs(os.path.dirname(archivo_tareas), exist_ok=True)
    with open(archivo_tareas, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)

def agregar_tarea(nombre, prioridad, descripcion, rol):
    nombre = nombre.strip()
    descripcion = descripcion.strip()
    rol = rol.strip()
    if nombre and rol:
        tareas.append({
            "nombre": nombre,
            "descripcion": descripcion,
            "prioridad": prioridad,
            "rol": rol,
            "asignada": False,
            "miembro": None,
            "estado": "pendiente"
        })
        guardar_datos_tareas()
        return True
    return False

def asignar_tareas_por_rol_y_prioridad(miembros):
    cargar_datos_tareas()
    no_asignadas = [t for t in tareas if not t["asignada"]]

    if not miembros or not no_asignadas:
        return 0  # nada que hacer

    # Inicializar conteo de tareas por miembro
    conteo = defaultdict(int)
    for t in tareas:
        if t["asignada"]:
            conteo[t["miembro"]] += 1

    prioridades = ["Alta", "Media", "Baja"]
    asignadas = 0

    for prioridad in prioridades:
        for tarea in [t for t in no_asignadas if t["prioridad"] == prioridad]:
            # Buscar miembros con el rol requerido
            disponibles = [m for m in miembros if m["rol"] == tarea["rol"]]
            if not disponibles:
                continue

            # Seleccionar el que tenga menos carga
            menos_cargado = min(disponibles, key=lambda m: conteo[m["nombre"]])
            tarea["asignada"] = True
            tarea["miembro"] = menos_cargado["nombre"]
            conteo[menos_cargado["nombre"]] += 1
            asignadas += 1
    print(f"Total de tareas asignadas: {asignadas}")
    guardar_datos_tareas()
    return asignadas