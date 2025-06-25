import openpyxl
from openpyxl.styles import Font
from datetime import datetime

def exportar_tareas_a_excel(tareas):
    if not tareas:
        return False, "No hay tareas para exportar."

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tareas"

    encabezados = ["Nombre", "Descripción", "Prioridad", "Estado", "Asignada", "Miembro", "Rol"]
    ws.append(encabezados)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for t in tareas:
        ws.append([
            t.get("nombre", t.get("descripcion", "")),
            t.get("descripcion", ""),
            t.get("prioridad", ""),
            t.get("estado", ""),
            "Sí" if t.get("asignada") else "No",
            t.get("miembro", ""),
            t.get("rol", "")
        ])

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_final = f"tareas_{timestamp}.xlsx"
    wb.save(nombre_final)
    return True, nombre_final