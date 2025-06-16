class Tarea:
    def __init__(self, descripcion, prioridad, rol_requerido):
        ...

class ColaTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea):
        ...
    
    def eliminar_tarea(self, index):
        ...
    
    def modificar_tarea(self, index, nueva_tarea):
        ...
    
    def obtener_todas(self):
        return self.tareas
    
