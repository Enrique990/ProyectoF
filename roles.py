import json
import os

archivo_roles = "datos/roles.json"
roles = []

def cargar_datos_roles():
    global roles
    if os.path.exists(archivo_roles):
        with open(archivo_roles, "r", encoding="utf-8") as f:
            roles = json.load(f)
    else:
        roles = []

def guardar_datos_roles():
    os.makedirs(os.path.dirname(archivo_roles), exist_ok=True)
    with open(archivo_roles, "w", encoding="utf-8") as f:
        json.dump(roles, f, indent=4, ensure_ascii=False)

def agregar_rol(nombre):
    nombre = nombre.strip()
    nombre = nombre.strip()
    if not nombre:
        return False
    # Comparación insensible a mayúsculas
    existentes = [r.lower() for r in roles]
    if nombre.lower() in existentes:
        return False
    # Guards el rol con formato uniforme, por ejemplo, capitalizado
    roles.append(nombre.capitalize())
    guardar_datos_roles()
    return True

def eliminar_rol(nombre):
    if nombre in roles:
        roles.remove(nombre)
        guardar_datos_roles()
        return True
    return False
