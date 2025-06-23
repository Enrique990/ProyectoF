from typing import List

class Persona:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol
        self.tareas = []

    def asignar_tarea(self, tarea):
        self.tareas.append(tarea)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "rol": self.rol,
            "tareas": self.tareas  # lista de strings
        }

    @staticmethod
    def from_dict(d):
        persona = Persona(d["nombre"], d["rol"])
        persona.tareas = d.get("tareas", [])
        return persona


class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []

    def agregar_miembro(self, persona):
        self.miembros.append(persona)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "miembros": [p.to_dict() for p in self.miembros]
        }

    @staticmethod
    def from_dict(d):
        equipo = Equipo(d["nombre"])
        equipo.miembros = [Persona.from_dict(m) for m in d.get("miembros", [])]
        return equipo


class Supervisor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.equipo = None  # instancia de Equipo

    def asignar_equipo(self, equipo):
        self.equipo = equipo

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "equipo": self.equipo.to_dict() if self.equipo else None
        }

    @staticmethod
    def from_dict(d):
        sup = Supervisor(d["nombre"])
        if "equipo" in d and d["equipo"]:
            sup.asignar_equipo(Equipo.from_dict(d["equipo"]))
        return sup

class Tarea:
    def __init__(self, descripcion, rol_requerido, prioridad="media", estado="sin asignar"):
        self.descripcion = descripcion
        self.rol_requerido = rol_requerido
        self.prioridad = prioridad  # "alta", "media", "baja"
        self.estado = estado        # "sin asignar", "en proceso", "finalizada"

    def to_dict(self):
        return {
            "descripcion": self.descripcion,
            "rol_requerido": self.rol_requerido,
            "prioridad": self.prioridad,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data):
        return Tarea(
            data["descripcion"],
            data["rol_requerido"],
            data.get("prioridad", "media"),
            data.get("estado", "sin asignar")
        )