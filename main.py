from equipo import Equipo
from tareas import ColaTareas
from gestor_tareas import Gestor
from excel_export import exportar_a_excel
from utils import limpiar_pantalla, pausar

# Crear instancias globales
equipo = Equipo()
cola = ColaTareas()
gestor = Gestor(equipo, cola)
