class Persona:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol
        self.hijos = []
        self.tareas_asignadas = []

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

class Equipo:
    def __init__(self):
        self.raiz = None

    def agregar_persona(self, nombre, rol, nombre_superior=None):
        ...
    
    def mostrar_estructura(self):
        ...
    
    def buscar_por_rol(self, nodo, nombre):
        ...