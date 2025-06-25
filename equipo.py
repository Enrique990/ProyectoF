from modelos import Supervisor, Equipo, Persona
from persistencia import guardar_equipo, cargar_equipo

# Lista en memoria con supervisores
supervisores = []

# Cargar datos al iniciar
def cargar_datos_equipo():
    global supervisores
    datos = cargar_equipo()
    supervisores = [Supervisor.from_dict(s) for s in datos]

# Guardar datos actualizados
def guardar_datos_equipo():
    datos = [s.to_dict() for s in supervisores]
    guardar_equipo(datos)

# Crear un nuevo supervisor
def crear_supervisor(nombre_supervisor, nombre_equipo):
    for s in supervisores:
        if s.nombre.lower() == nombre_supervisor.lower():
            return False  # Supervisor ya existe
        if s.equipo and s.equipo.nombre.lower() == nombre_equipo.lower():
            return False  # Nombre de equipo duplicado

    supervisor = Supervisor(nombre_supervisor)
    equipo_obj = Equipo(nombre_equipo)
    supervisor.asignar_equipo(equipo_obj)
    supervisores.append(supervisor)
    guardar_datos_equipo()
    return True

# Agregar un miembro a un equipo
def agregar_miembro(nombre_supervisor, nombre_persona, rol):
    # Verifica si ya existe ese nombre en cualquier equipo
    for s in supervisores:
        if s.equipo:
            for m in s.equipo.miembros:
                if m.nombre.lower() == nombre_persona.lower():
                    return False  # Ya existe
    for s in supervisores:
        if s.nombre.lower() == nombre_supervisor.lower():
            persona = Persona(nombre_persona, rol)
            s.equipo.agregar_miembro(persona)
            guardar_datos_equipo()
            return True
    return False

# Listar toda la estructura
def mostrar_estructura():
    for s in supervisores:
        print(f"Supervisor: {s.nombre}")
        if s.equipo:
            print(f"  Equipo: {s.equipo.nombre}")
            for m in s.equipo.miembros:
                print(f"    Miembro: {m.nombre} (rol: {m.rol}, tareas: {len(m.tareas)})")
        else:
            print("  (sin equipo asignado)")

# Eliminar supervisor
def eliminar_supervisor(nombre):
    global supervisores
    for s in supervisores:
        if s.nombre.strip().lower() == nombre.strip().lower():
            supervisores.remove(s)
            guardar_datos_equipo()
            return True
    return False

# Eliminar miembro
def eliminar_miembro(nombre_supervisor, nombre_miembro):
    for s in supervisores:
        if s.nombre == nombre_supervisor and s.equipo:
            s.equipo.miembros = [
                m for m in s.equipo.miembros if m.nombre != nombre_miembro
            ]
            guardar_datos_equipo()
            return True
    return False

# Modificar rol de miembro
def modificar_rol_miembro(nombre_supervisor, nombre_miembro, nuevo_rol):
    for s in supervisores:
        if s.nombre.lower() == nombre_supervisor.lower():
            for m in s.equipo.miembros:
                if m.nombre.lower() == nombre_miembro.lower():
                    m.rol = nuevo_rol
                    guardar_datos_equipo()
                    return True
    return False

def obtener_todos_los_miembros(equipo):
    return [{"nombre": m.nombre, "rol": m.rol} for m in equipo.miembros]