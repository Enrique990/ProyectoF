from persistencia import cargar_roles, guardar_roles

def listar_roles():
    """Devuelve la lista actual de roles."""
    return cargar_roles()

def crear_rol(nuevo_rol):
    """Agrega un nuevo rol si no existe aún."""
    roles = cargar_roles()
    if nuevo_rol not in roles:
        roles.append(nuevo_rol)
        guardar_roles(roles)
        return True
    return False  # El rol ya existe

def eliminar_rol(nombre_rol):
    """Elimina un rol por nombre si existe."""
    roles = cargar_roles()
    if nombre_rol in roles:
        roles = [r for r in roles if r != nombre_rol]
        guardar_roles(roles)
        return True
    return False  # El rol no estaba