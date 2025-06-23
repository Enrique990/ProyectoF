from persistencia import cargar_tareas, guardar_tareas, cargar_equipo, guardar_equipo
from modelos import Tarea, Persona, Supervisor
from equipo import supervisores  # asumimos que ya se cargaron desde equipo

# Crear y agregar tarea a la lista general
def crear_tarea(descripcion, rol_requerido, prioridad="media"):
    nueva = Tarea(descripcion, rol_requerido, prioridad, estado="sin asignar")
    tareas = [Tarea.from_dict(t) for t in cargar_tareas()]
    tareas.append(nueva)
    guardar_tareas([t.to_dict() for t in tareas])

# Listar tareas actuales
def listar_tareas():
    return [Tarea.from_dict(t) for t in cargar_tareas()]

# Asignar automáticamente tareas no asignadas
def asignar_tareas():
    tareas = [Tarea.from_dict(t) for t in cargar_tareas()]
    pendientes = [t for t in tareas if t.estado == "sin asignar"]

    for tarea in pendientes:
        for s in supervisores:
            equipo = s.equipo
            if not equipo:
                continue

            posibles = [p for p in equipo.miembros if p.rol == tarea.rol_requerido]
            if not posibles:
                continue

            menos_ocupado = min(posibles, key=lambda p: len(p.tareas))
            menos_ocupado.asignar_tarea(tarea.descripcion)
            tarea.estado = "en proceso"
            break  # tarea asignada, salimos del bucle

    guardar_tareas([t.to_dict() for t in tareas])
    guardar_equipo([s.to_dict() for s in supervisores])

# Cambiar estado de una tarea
def cambiar_estado_tarea(indice, nuevo_estado):
    tareas = [Tarea.from_dict(t) for t in cargar_tareas()]
    if 0 <= indice < len(tareas):
        tareas[indice].estado = nuevo_estado
        guardar_tareas([t.to_dict() for t in tareas])

# Cambiar prioridad de una tarea
def cambiar_prioridad_tarea(indice, nueva_prioridad):
    tareas = [Tarea.from_dict(t) for t in cargar_tareas()]
    if 0 <= indice < len(tareas):
        tareas[indice].prioridad = nueva_prioridad
        guardar_tareas([t.to_dict() for t in tareas])

# Eliminar tarea
def eliminar_tarea(indice):
    tareas = [Tarea.from_dict(t) for t in cargar_tareas()]
    if 0 <= indice < len(tareas):
        tareas.pop(indice)
        guardar_tareas([t.to_dict() for t in tareas])