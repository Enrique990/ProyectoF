import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import equipo, roles, tareas
import json
from modelos import Equipo , Supervisor
from excel_export import exportar_tareas_a_excel

# Cargar supervisor desde archivo JSON
with open("datos/equipo.json", "r", encoding="utf-8") as archivo:
    supervisor_raw = json.load(archivo)
    equipos = [Supervisor.from_dict(d) for d in supervisor_raw]

# ==== Ventana principal ====
ventana = tk.Tk()
ventana.title("TaskTree - Menú Principal")
ventana.geometry("400x400")

# Contenedor principal
contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

# Diccionario de frames
frames = {}

# ==== Función para mostrar cualquier menú ====
def mostrar_frame(nombre):
    for f in frames.values():
        f.pack_forget()
    frames[nombre].pack(fill="both", expand=True)

# ==== MENÚ PRINCIPAL ====
def crear_menu_principal():
    frame = tk.Frame(contenedor)
    frames["principal"] = frame

    tk.Label(frame, text="Menú Principal", font=("Helvetica", 18)).pack(pady=20)

    tk.Button(frame, text="Menú Equipo", width=30, command=lambda: mostrar_frame("equipo")).pack(pady=5)
    tk.Button(frame, text="Menú Tareas", width=30, command=lambda: mostrar_frame("tareas")).pack(pady=5)
    tk.Button(frame, text="Menú Roles", width=30, command=lambda: mostrar_frame("roles")).pack(pady=5)
    tk.Button(frame, text="Salir", width=30, command=ventana.destroy).pack(pady=20)

# ==== MENÚ EQUIPO ====
def crear_menu_equipo():
    frame = tk.Frame(contenedor)
    frames["equipo"] = frame

    tk.Label(frame, text="Gestión de Equipo", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(frame, text="Menú Supervisores", width=25, command=lambda: mostrar_frame("supervisores")).pack(pady=3)
    tk.Button(frame, text="Menú Miembros", width=25, command=lambda: mostrar_frame("miembros")).pack(pady=3)

    # Mostrar estructura
    def mostrar_estructura_equipo():
        equipo.cargar_datos_equipo()
        ventana_arbol = Toplevel()
        ventana_arbol.title("Estructura del Equipo")
        ventana_arbol.geometry("400x300")

        tree = ttk.Treeview(ventana_arbol)
        tree.heading("#0", text="Estructura", anchor="w")
        tree.pack(fill="both", expand=True)

        for s in equipo.supervisores:
            id_sup = tree.insert("", "end", text=f"Supervisor: {s.nombre}")
            if s.equipo:
                id_eq = tree.insert(id_sup, "end", text=f"Equipo: {s.equipo.nombre}")
                for m in s.equipo.miembros:
                    tree.insert(id_eq, "end", text=f"{m.nombre} (rol: {m.rol}, tareas: {len(m.tareas)})")
    tk.Button(frame, text="Ver estructura del equipo", width=25, command=mostrar_estructura_equipo).pack(pady=3)
    tk.Button(frame, text="Gestión de roles", width=25, command=lambda: mostrar_frame("roles")).pack(pady=3)
    tk.Button(frame, text="Volver al Menú Principal", width=25, command=lambda: mostrar_frame("principal")).pack(pady=10)


# ==== MENÚ TAREAS ====
def crear_menu_tareas():
    frame = tk.Frame(contenedor)
    frames["tareas"] = frame

    tk.Label(frame, text="Menú Tareas", font=("Helvetica", 16)).pack(pady=10)

    # Agregar tarea a la cola
    def mostrar_formulario_agregar_tarea():
        tareas.cargar_datos_tareas()
        roles.cargar_datos_roles()

        ventana = Toplevel()
        ventana.title("Agregar Tarea a la Cola")
        ventana.geometry("300x380")

        tk.Label(ventana, text="Nombre de la tarea:").pack(pady=5)
        entrada = tk.Entry(ventana)
        entrada.pack()

        tk.Label(ventana, text="Descripción:").pack(pady=5)
        texto = tk.Text(ventana, height=4, width=30)
        texto.pack()

        tk.Label(ventana, text="Rol requerido:").pack(pady=5)
        rol_var = tk.StringVar()
        combo_rol = ttk.Combobox(ventana, textvariable=rol_var, state="readonly")
        combo_rol["values"] = roles.roles
        combo_rol.pack()

        tk.Label(ventana, text="Prioridad:").pack(pady=5)
        prioridad_var = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=prioridad_var, state="readonly")
        combo["values"] = ["Alta", "Media", "Baja"]
        combo.pack()

        mensaje = tk.Label(ventana, text="", fg="green")
        mensaje.pack(pady=5)

        def agregar():
            nombre = entrada.get().strip()
            descripcion = texto.get("1.0", tk.END)
            rol = rol_var.get().strip()
            prioridad = prioridad_var.get()
            if not nombre or not prioridad or not descripcion or not rol:
                mensaje.config(text="Completá todos los campos.", fg="red")
                return
            
            exito = tareas.agregar_tarea(nombre, prioridad, descripcion, rol)
            if exito:
                mensaje.config(text="Tarea agregada con éxito.", fg="green")
                entrada.delete(0, tk.END)
                combo.set("")
                texto.delete("1.0", tk.END)
            else:
                mensaje.config(text="Nombre inválido o duplicado.", fg="red")
        tk.Button(ventana, text="Agregar", command=agregar).pack(pady=10)
    tk.Button(frame, text="Agregar tarea a la cola", width=30, command=mostrar_formulario_agregar_tarea).pack(pady=2)
    
    # Ver tareas en cola
    def mostrar_cola_tareas():
        tareas.cargar_datos_tareas()
        tareas_no_asignadas = [t for t in tareas.tareas if not t["asignada"]]

        if not tareas_no_asignadas:
            messagebox.showinfo("Sin tareas", "La cola de tareas está vacía.")
            return

        ventana = Toplevel()
        ventana.title("Cola de Tareas")
        ventana.geometry("500x350")

        tk.Label(ventana, text="Tareas sin asignar", font=("Helvetica", 12)).pack(pady=5)

        area = tk.Text(ventana, width=60, height=15)
        area.pack(padx=10)
        for t in tareas_no_asignadas:
            area.insert(tk.END,
                f"- {t['nombre']}\n"
                f"  Prioridad: {t['prioridad']} | Estado: {t['estado']} | Rol requerido: {t['rol']}\n"
                f"  Descripción: {t['descripcion']}\n\n"
            )
        area.config(state=tk.DISABLED)
    tk.Button(frame, text="Ver cola de tareas", width=30, command=mostrar_cola_tareas).pack(pady=2)
    
    # Eliminar tarea
    def mostrar_formulario_eliminar_tarea():
        tareas.cargar_datos_tareas()
        lista_tareas = tareas.tareas.copy()

        if not lista_tareas:
            messagebox.showinfo("Sin tareas", "No hay tareas para eliminar.")
            return

        ventana = Toplevel()
        ventana.title("Eliminar Tarea")
        ventana.geometry("400x250")

        tk.Label(ventana, text="Seleccioná una tarea a eliminar:").pack(pady=5)

        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly", width=45)

        # Mostrar asignación en la descripción
        def descripcion_tarea(t):
            asignada = f"Asignada a {t['miembro']}" if t["asignada"] else "Sin asignar"
            return f"{t['nombre']} ({asignada})"

        opciones = [descripcion_tarea(t) for t in lista_tareas]
        combo["values"] = opciones
        combo.pack(pady=5)

        mensaje = tk.Label(ventana, text="", fg="red")
        mensaje.pack(pady=5)

        def eliminar():
            seleccion_texto = seleccion.get()
            if not seleccion_texto:
                mensaje.config(text="Seleccioná una tarea.", fg="red")
                return

            nombre_tarea = seleccion_texto.split(" (")[0]

            for t in tareas.tareas:
                if t["nombre"] == nombre_tarea:
                    confirmar = messagebox.askyesno(
                        "Confirmación",
                        f"¿Estás seguro de eliminar la tarea \"{t['nombre']}\"?"
                    )
                    if confirmar:
                        tareas.tareas.remove(t)
                        tareas.guardar_datos_tareas()
                        mensaje.config(text="Tarea eliminada con éxito.", fg="green")
                        combo["values"] = [descripcion_tarea(t) for t in tareas.tareas]
                        combo.set("")
                    return

            mensaje.config(text="No se pudo eliminar la tarea.", fg="red")

        tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=10)
    tk.Button(frame, text="Eliminar una tarea", width=30, command=mostrar_formulario_eliminar_tarea).pack(pady=2)
    
    # Modificar tarea sin asignar
    def mostrar_modificar_tarea_no_asignada():
        tareas.cargar_datos_tareas()
        roles.cargar_datos_roles()
        tareas_pendientes = [t for t in tareas.tareas if not t["asignada"]]

        if not tareas_pendientes:
            messagebox.showinfo("Sin tareas", "No hay tareas sin asignar para modificar.")
            return

        ventana = Toplevel()
        ventana.title("Modificar Tarea (no asignada)")
        ventana.geometry("350x400")

        tk.Label(ventana, text="Seleccioná una tarea:").pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly", width=35)
        combo["values"] = [t["nombre"] for t in tareas_pendientes]
        combo.pack(pady=5)

        tk.Label(ventana, text="Nuevo nombre:").pack()
        entrada_nombre = tk.Entry(ventana, width=35)
        entrada_nombre.pack(pady=2)

        tk.Label(ventana, text="Nuevo rol requerido:").pack()
        rol_var = tk.StringVar()
        combo_rol = ttk.Combobox(ventana, textvariable=rol_var, state="readonly")
        combo_rol["values"] = roles.roles
        combo_rol.pack(pady=2)

        tk.Label(ventana, text="Nueva prioridad:").pack()
        prioridad_var = tk.StringVar()
        combo_prioridad = ttk.Combobox(ventana, textvariable=prioridad_var, state="readonly")
        combo_prioridad["values"] = ["Alta", "Media", "Baja"]
        combo_prioridad.pack(pady=2)

        tk.Label(ventana, text="Nueva descripción:").pack()
        texto = tk.Text(ventana, height=5, width=35)
        texto.pack(pady=2)

        mensaje = tk.Label(ventana, text="", fg="red")
        mensaje.pack(pady=5)

        def cargar_info(event):
            nombre = seleccion.get()
            for t in tareas_pendientes:
                if t["nombre"] == nombre:
                    entrada_nombre.delete(0, tk.END)
                    entrada_nombre.insert(0, t["nombre"])
                    combo_rol.set(t["rol"])
                    combo_prioridad.set(t["prioridad"])
                    texto.delete("1.0", tk.END)
                    texto.insert(tk.END, t["descripcion"])
                    break

        combo.bind("<<ComboboxSelected>>", cargar_info)

        def modificar():
            nombre_actual = seleccion.get()
            nuevo_nombre = entrada_nombre.get().strip()
            nuevo_rol = rol_var.get().strip()
            nueva_prioridad = prioridad_var.get().strip()
            nueva_descripcion = texto.get("1.0", tk.END).strip()

            if not nombre_actual or not nuevo_nombre or not nueva_prioridad or not nueva_descripcion or not nuevo_rol:
                mensaje.config(text="Completá todos los campos.", fg="red")
                return

            for t in tareas.tareas:
                if t["nombre"] == nombre_actual and not t["asignada"]:
                    t["nombre"] = nuevo_nombre
                    t["rol"] = nuevo_rol
                    t["prioridad"] = nueva_prioridad
                    t["descripcion"] = nueva_descripcion
                    tareas.guardar_datos_tareas()
                    mensaje.config(text="Tarea modificada exitosamente.", fg="green")
                    combo["values"] = [t["nombre"] for t in tareas.tareas if not t["asignada"]]
                    combo.set("")
                    entrada_nombre.delete(0, tk.END)
                    combo_prioridad.set("")
                    texto.delete("1.0", tk.END)
                    return

            mensaje.config(text="No se pudo modificar la tarea.", fg="red")

        tk.Button(ventana, text="Guardar cambios", command=modificar).pack(pady=10)
    tk.Button(frame, text="Modificar tarea sin asignar", width=30, command=mostrar_modificar_tarea_no_asignada).pack(pady=2)
    
    # Modificar tarea asignada
    def mostrar_modificar_tarea_asignada():
        tareas.cargar_datos_tareas()
        tareas_asignadas = [t for t in tareas.tareas if t["asignada"]]

        if not tareas_asignadas:
            messagebox.showinfo("Sin tareas", "No hay tareas asignadas para modificar.")
            return

        ventana = Toplevel()
        ventana.title("Modificar Tarea Asignada")
        ventana.geometry("350x250")

        tk.Label(ventana, text="Seleccioná una tarea asignada:").pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly", width=35)
        combo["values"] = [f"{t['nombre']} ({t['miembro']})" for t in tareas_asignadas]
        combo.pack(pady=5)

        tk.Label(ventana, text="Nuevo estado:").pack()
        estado_var = tk.StringVar()
        combo_estado = ttk.Combobox(ventana, textvariable=estado_var, state="readonly")
        combo_estado["values"] = ["pendiente", "en proceso", "finalizada"]
        combo_estado.pack(pady=5)

        mensaje = tk.Label(ventana, text="", fg="green")
        mensaje.pack(pady=5)

        def modificar_estado():
            seleccion_texto = seleccion.get()
            nuevo_estado = estado_var.get()

            if not seleccion_texto or not nuevo_estado:
                mensaje.config(text="Seleccioná una tarea y un estado.", fg="red")
                return

            nombre_tarea = seleccion_texto.split(" (")[0]

            for t in tareas.tareas:
                if t["nombre"] == nombre_tarea and t["asignada"]:
                    if nuevo_estado == "finalizada":
                        confirmar = messagebox.askyesno(
                            "Confirmar finalización",
                            "¿Estás seguro que querés marcar esta tarea como FINALIZADA? Esto la eliminará del sistema."
                        )
                        if confirmar:
                            tareas.tareas.remove(t)
                            tareas.guardar_datos_tareas()
                            mensaje.config(text="Tarea finalizada y eliminada.", fg="green")
                            combo["values"] = [f"{t['nombre']} ({t['miembro']})" for t in tareas.tareas if t["asignada"]]
                            combo.set("")
                            combo_estado.set("")
                        return
                    else:
                        t["estado"] = nuevo_estado
                        tareas.guardar_datos_tareas()
                        mensaje.config(text="Estado actualizado exitosamente.", fg="green")
                        return

            mensaje.config(text="No se pudo modificar la tarea.", fg="red")

        tk.Button(ventana, text="Guardar cambios", command=modificar_estado).pack(pady=10)
    tk.Button(frame, text="Modificar tarea asignada", width=30, command=mostrar_modificar_tarea_asignada).pack(pady=2)

    # Asignar tareas automáticamente
    def asignar_tareas_automaticamente():
        equipo.cargar_datos_equipo()
        miembros = equipo.obtener_todos_los_miembros(equipos)  # Esta debe devolver lista de dicts con nombre y rol
        for persona in miembros:
            print(f"Miembro: {persona['nombre']} (rol: {persona['rol']})")

        if not miembros:
            messagebox.showinfo("Equipo vacío", "No hay miembros en el equipo.")
            return

        cantidad = tareas.asignar_tareas_por_rol_y_prioridad(miembros)
        if cantidad > 0:
            messagebox.showinfo("Asignación completa", f"Se asignaron {cantidad} tarea(s) automáticamente.")
        else:
            messagebox.showinfo("Sin asignaciones", "No hay tareas que se puedan asignar.")
    tk.Button(frame, text="Asignar tareas automáticamente", width=30, command=asignar_tareas_automaticamente).pack(pady=2)
    
    # Ver tareas asignadas por persona
    def mostrar_tareas_por_persona():
        equipos.equipo  # Ya debería estar cargado
        miembros = equipos.equipo.miembros

        if not miembros:
            messagebox.showinfo("Equipo vacío", "No hay miembros para mostrar.")
            return

        ventana = Toplevel()
        ventana.title("Tareas por Persona")
        ventana.geometry("500x400")

        tk.Label(ventana, text="Seleccioná un miembro:").pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly")
        combo["values"] = [m.nombre for m in miembros]
        combo.pack(pady=5)

        area = tk.Text(ventana, width=60, height=12)
        area.pack(pady=5)

        combo_tareas = ttk.Combobox(ventana, state="readonly")
        combo_tareas.pack(pady=2)

        mensaje = tk.Label(ventana, text="", fg="green")
        mensaje.pack(pady=5)

        def mostrar_tareas(event=None):
            nombre = seleccion.get()
            area.config(state=tk.NORMAL)
            area.delete("1.0", tk.END)
            combo_tareas.set("")
            combo_tareas["values"] = []

            tareas.cargar_datos_tareas()
            tareas_persona = [t for t in tareas.tareas if t["asignada"] and t["miembro"] == nombre]

            for t in tareas_persona:
                area.insert(tk.END,
                    f"- {t['nombre']} (Prioridad: {t['prioridad']}, Estado: {t['estado']}, Rol: {t['rol']})\n"
                    f"  {t['descripcion']}\n\n"
                )
            area.config(state=tk.DISABLED)

            combo_tareas["values"] = [t["nombre"] for t in tareas_persona]

        combo.bind("<<ComboboxSelected>>", mostrar_tareas)

        def finalizar_tarea():
            nombre = seleccion.get()
            nombre_tarea = combo_tareas.get()

            if not nombre or not nombre_tarea:
                mensaje.config(text="Seleccioná una persona y una tarea.", fg="red")
                return

            for t in tareas.tareas:
                if t["nombre"] == nombre_tarea and t["miembro"] == nombre and t["asignada"]:
                    confirmar = messagebox.askyesno(
                        "Confirmar finalización",
                        f"¿Seguro que querés finalizar la tarea \"{t['nombre']}\"?"
                    )
                    if confirmar:
                        tareas.tareas.remove(t)
                        tareas.guardar_datos_tareas()
                        mensaje.config(text="Tarea finalizada y eliminada.", fg="green")
                        mostrar_tareas()
                    return

            mensaje.config(text="No se pudo finalizar la tarea.", fg="red")

        tk.Button(ventana, text="Marcar como finalizada", command=finalizar_tarea).pack(pady=4)
    tk.Button(frame, text="Ver tareas asignadas por persona", width=30, command=mostrar_tareas_por_persona).pack(pady=2)
    
    # Exportar informe a Excel
    def exportar_tareas():
        tareas.cargar_datos_tareas()
        exito, resultado = exportar_tareas_a_excel(tareas.tareas)
        if exito:
            messagebox.showinfo("Exportación exitosa", f"Tareas exportadas a: {resultado}")
        else:
            messagebox.showinfo("Sin datos", resultado)
    tk.Button(frame, text="Exportar informe", width=30, command=exportar_tareas).pack(pady=2)
    
    tk.Button(frame, text="Volver al Menú Principal", width=30, command=lambda: mostrar_frame("principal")).pack(pady=10)

# ==== MENÚ SUPERVISOR ====
def crear_menu_supervisores():
    frame = tk.Frame(contenedor)
    frames["supervisores"] = frame

    tk.Label(frame, text="Menú Supervisores", font=("Helvetica", 16)).pack(pady=10)

    # Crear nuevo supervisor
    def mostrar_formulario_supervisor():
        ventana_sup = Toplevel()
        ventana_sup.title("Crear Supervisor")
        ventana_sup.geometry("300x200")

        tk.Label(ventana_sup, text="Nombre del supervisor:").pack(pady=2)
        entrada_sup = tk.Entry(ventana_sup)
        entrada_sup.pack()

        tk.Label(ventana_sup, text="Nombre del equipo:").pack(pady=2)
        entrada_eq = tk.Entry(ventana_sup)
        entrada_eq.pack()

        mensaje = tk.Label(ventana_sup, text="", fg="green")
        mensaje.pack(pady=5)

        def procesar_creacion():
            nombre_sup = entrada_sup.get().strip()
            nombre_eq = entrada_eq.get().strip()
        
            if not nombre_sup or not nombre_eq:
                mensaje.config(text="Completa ambos campos.", fg="red")
                return
        
            exito = equipo.crear_supervisor(nombre_sup, nombre_eq)
            if exito:
                equipo.cargar_datos_equipo()
                mensaje.config(text="Supervisor creado con equipo asignado.", fg="green")
                entrada_sup.delete(0, tk.END)
                entrada_eq.delete(0, tk.END)
            else:
                mensaje.config(text="Ese supervisor o equipo ya existe.", fg="red")


        tk.Button(ventana_sup, text="Crear", command=procesar_creacion).pack(pady=10)
    tk.Button(frame, text="Crear nuevo supervisor", width=30, command=mostrar_formulario_supervisor).pack(pady=3)

    # Listar supervisores
    def mostrar_lista_supervisores():
        equipo.cargar_datos_equipo()
        supervisores = equipo.supervisores

        if not supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores registrados.")
            return

        ventana_ver = Toplevel()
        ventana_ver.title("Supervisores Registrados")
        ventana_ver.geometry("350x250")

        tk.Label(ventana_ver, text="Lista de Supervisores", font=("Helvetica", 14)).pack(pady=8)

        texto = tk.Text(ventana_ver, width=40, height=10)
        texto.pack(padx=10)

        for s in supervisores:
            nombre_eq = s.equipo.nombre if s.equipo else "Sin equipo"
            texto.insert(tk.END, f"Supervisor: {s.nombre}  →  Equipo: {nombre_eq}\n")

        texto.config(state=tk.DISABLED)
    tk.Button(frame, text="Ver supervisores", width=30, command=mostrar_lista_supervisores).pack(pady=3)

    # Eliminar supervisor
    def mostrar_eliminacion_supervisor():
        equipo.cargar_datos_equipo()
        supervisores = equipo.supervisores
        if not supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores para eliminar.")
            return

        ventana_eliminar = Toplevel()
        ventana_eliminar.title("Eliminar Supervisor")
        ventana_eliminar.geometry("320x200")

        tk.Label(ventana_eliminar, text="Selecciona un supervisor:").pack(pady=3)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana_eliminar, textvariable=seleccion, state="readonly")
        combo["values"] = [s.nombre for s in supervisores]
        combo.pack(pady=5)

        mensaje = tk.Label(ventana_eliminar, text="", fg="red")
        mensaje.pack(pady=5)

        def eliminar():
            supervisores = equipo.supervisores
            nombre = seleccion.get()
            if not nombre:
                mensaje.config(text="Seleccioná un supervisor.")
                return

            for s in supervisores:
                if s.nombre == nombre and s.equipo and s.equipo.miembros:
                    respuesta = messagebox.askyesno("Equipo con miembros",
                        f"El supervisor '{nombre}' tiene un equipo con miembros.\n¿Querés eliminar todo el equipo y sus miembros?")
                    if not respuesta:
                        mensaje.config(text="Eliminación cancelada.")
                        return

            exito = equipo.eliminar_supervisor(nombre)
            if exito:
                equipo.cargar_datos_equipo()  # ← Recarga datos actualizados
                supervisores = equipo.supervisores  # ← Refresca la lista local

                mensaje.config(text="Supervisor eliminado correctamente.", fg="green")
                combo["values"] = [s.nombre for s in supervisores]
                combo.set("")
            else:
                mensaje.config(text="No se pudo eliminar el supervisor.", fg="red")
        tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).pack(pady=10)

    tk.Button(frame, text="Eliminar supervisor", width=30, command=mostrar_eliminacion_supervisor).pack(pady=3)

    tk.Button(frame, text="Volver al menú Equipo", width=30, command=lambda: mostrar_frame("equipo")).pack(pady=10)

# ==== MENÚ MIEMBROS ====
def crear_menu_miembros():
    frame = tk.Frame(contenedor)
    frames["miembros"] = frame

    tk.Label(frame, text="Menú Miembros", font=("Helvetica", 16)).pack(pady=10)

    # Agregar miembro
    def mostrar_formulario_miembro():
        equipo.cargar_datos_equipo()
        roles.cargar_datos_roles()

        if not equipo.supervisores:
            messagebox.showwarning("Sin supervisores", "Primero debés crear un supervisor.")
            return

        if not roles.roles:
            messagebox.showwarning("Sin roles", "Primero debés agregar al menos un rol.")
            return

        ventana_miembro = Toplevel()
        ventana_miembro.title("Agregar Miembro")
        ventana_miembro.geometry("300x260")

        tk.Label(ventana_miembro, text="Supervisor:").pack(pady=2)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(ventana_miembro, textvariable=supervisor_var, state="readonly")
        supervisor_combo["values"] = [s.nombre for s in equipo.supervisores]
        supervisor_combo.pack()

        tk.Label(ventana_miembro, text="Nombre del miembro:").pack(pady=2)
        entrada_nombre = tk.Entry(ventana_miembro)
        entrada_nombre.pack()

        tk.Label(ventana_miembro, text="Rol:").pack(pady=2)
        rol_var = tk.StringVar()
        rol_combo = ttk.Combobox(ventana_miembro, textvariable=rol_var, state="readonly")
        rol_combo["values"] = roles.roles
        rol_combo.pack()

        mensaje = tk.Label(ventana_miembro, text="", fg="green")
        mensaje.pack(pady=5)

        def procesar_agregado():
            sup = supervisor_var.get().strip()
            nombre = entrada_nombre.get().strip()
            rol = rol_var.get().strip()

            if not sup or not nombre or not rol:
                mensaje.config(text="Completa todos los campos.", fg="red")
                return

            exito = equipo.agregar_miembro(sup, nombre, rol)
            if exito:
                mensaje.config(text="Miembro agregado correctamente.", fg="green")
                supervisor_combo.set("")
                entrada_nombre.delete(0, tk.END)
                rol_combo.set("")
            else:
                mensaje.config(text="Nombre duplicado o supervisor no encontrado.", fg="red")

        tk.Button(ventana_miembro, text="Agregar", command=procesar_agregado).pack(pady=10)
    tk.Button(frame, text="Agregar miembro", width=30, command=mostrar_formulario_miembro).pack(pady=3)

    # Ver miembros
    def mostrar_lista_miembros():
        equipo.cargar_datos_equipo()
        if not equipo.supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores disponibles.")
            return

        ventana_ver = Toplevel()
        ventana_ver.title("Ver Miembros por Supervisor")
        ventana_ver.geometry("350x280")

        tk.Label(ventana_ver, text="Seleccioná un supervisor:", font=("Helvetica", 10)).pack(pady=5)
        var_sup = tk.StringVar()
        combo = ttk.Combobox(ventana_ver, textvariable=var_sup, state="readonly")
        combo["values"] = [s.nombre for s in equipo.supervisores]
        combo.pack()

        area_texto = tk.Text(ventana_ver, width=40, height=10)
        area_texto.pack(pady=8)
        area_texto.config(state=tk.DISABLED)

        def mostrar():
            nombre = var_sup.get()
            for s in equipo.supervisores:
                if s.nombre == nombre and s.equipo:
                    miembros = s.equipo.miembros
                    area_texto.config(state=tk.NORMAL)
                    area_texto.delete("1.0", tk.END)
                    if miembros:
                        for m in miembros:
                            area_texto.insert(tk.END, f"{m.nombre} - Rol: {m.rol} (Tareas: {len(m.tareas)})\n")
                    else:
                        area_texto.insert(tk.END, "Este equipo no tiene miembros.")
                    area_texto.config(state=tk.DISABLED)
                    return
        tk.Button(ventana_ver, text="Mostrar miembros", command=mostrar).pack()
    tk.Button(frame, text="Ver miembros", width=30, command=mostrar_lista_miembros).pack(pady=3)

    # Eliminar miembro
    def mostrar_formulario_eliminar_miembro():
        equipo.cargar_datos_equipo()
        if not equipo.supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores disponibles.")
            return

        ventana_eliminar = Toplevel()
        ventana_eliminar.title("Eliminar Miembro")
        ventana_eliminar.geometry("300x220")

        tk.Label(ventana_eliminar, text="Supervisor:").pack(pady=2)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(ventana_eliminar, textvariable=supervisor_var, state="readonly")
        supervisor_combo["values"] = [s.nombre for s in equipo.supervisores]
        supervisor_combo.pack()

        tk.Label(ventana_eliminar, text="Miembro:").pack(pady=2)
        miembro_var = tk.StringVar()
        miembro_combo = ttk.Combobox(ventana_eliminar, textvariable=miembro_var, state="readonly")
        miembro_combo.pack()

        mensaje = tk.Label(ventana_eliminar, text="", fg="green")
        mensaje.pack(pady=5)

        def actualizar_miembros(event):
            nombre_sup = supervisor_var.get()
            for s in equipo.supervisores:
                if s.nombre == nombre_sup and s.equipo:
                    miembros = [m.nombre for m in s.equipo.miembros]
                    miembro_combo["values"] = miembros
                    miembro_combo.set("")
                    return
            miembro_combo["values"] = []
            miembro_combo.set("")

        supervisor_combo.bind("<<ComboboxSelected>>", actualizar_miembros)

        def procesar_eliminacion():
            nombre_sup = supervisor_var.get()
            nombre_miembro = miembro_var.get()
            if not nombre_sup or not nombre_miembro:
                mensaje.config(text="Selecciona supervisor y miembro.", fg="red")
                return
            confirmado = equipo.eliminar_miembro(nombre_sup, nombre_miembro)
            if confirmado:
                mensaje.config(text="Miembro eliminado.", fg="green")
                supervisor_combo.set("")
                actualizar_miembros(None)
            else:
                mensaje.config(text="No se pudo eliminar.", fg="red")

        tk.Button(ventana_eliminar, text="Eliminar", command=procesar_eliminacion).pack(pady=10)
    tk.Button(frame, text="Eliminar miembro", width=30, command=mostrar_formulario_eliminar_miembro).pack(pady=3)
    
    # Modificar miembro
    def mostrar_formulario_modificar_miembro():
        equipo.cargar_datos_equipo()
        roles.cargar_datos_roles()

        if not equipo.supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores disponibles.")
            return

        if not roles.roles:
            messagebox.showinfo("Sin roles", "No hay roles disponibles. Agregá uno primero.")
            return

        ventana_mod = Toplevel()
        ventana_mod.title("Modificar Miembro")
        ventana_mod.geometry("300x270")

        tk.Label(ventana_mod, text="Supervisor:").pack(pady=2)
        var_sup = tk.StringVar()
        combo_sup = ttk.Combobox(ventana_mod, textvariable=var_sup, state="readonly")
        combo_sup["values"] = [s.nombre for s in equipo.supervisores]
        combo_sup.pack()

        tk.Label(ventana_mod, text="Miembro:").pack(pady=2)
        var_miembro = tk.StringVar()
        combo_miembro = ttk.Combobox(ventana_mod, textvariable=var_miembro, state="readonly")
        combo_miembro.pack()

        tk.Label(ventana_mod, text="Nuevo rol:").pack(pady=2)
        var_rol = tk.StringVar()
        combo_rol = ttk.Combobox(ventana_mod, textvariable=var_rol, state="readonly")
        combo_rol["values"] = roles.roles
        combo_rol.pack()

        mensaje = tk.Label(ventana_mod, text="", fg="green")
        mensaje.pack(pady=5)

        def actualizar_miembros(event):
            nombre = var_sup.get()
            for s in equipo.supervisores:
                if s.nombre == nombre and s.equipo:
                    combo_miembro["values"] = [m.nombre for m in s.equipo.miembros]
                    combo_miembro.set("")
                    return
            combo_miembro["values"] = []
            combo_miembro.set("")

        combo_sup.bind("<<ComboboxSelected>>", actualizar_miembros)

        def modificar():
            sup = var_sup.get()
            persona = var_miembro.get()
            nuevo_rol = var_rol.get().strip()

            if not sup or not persona or not nuevo_rol:
                mensaje.config(text="Completa todos los campos.", fg="red")
                return

            resultado = equipo.modificar_rol_miembro(sup, persona, nuevo_rol)
            if resultado:
                mensaje.config(text="Rol actualizado correctamente.", fg="green")
                combo_sup.set("")
                combo_miembro["values"] = []
                combo_miembro.set("")
                combo_rol.set("")
            else:
                mensaje.config(text="No se pudo actualizar el rol.", fg="red")

        tk.Button(ventana_mod, text="Modificar", command=modificar).pack(pady=10)
    tk.Button(frame, text="Modificar miembro", width=30, command=mostrar_formulario_modificar_miembro).pack(pady=3)

    tk.Button(frame, text="Volver al menú Equipo", width=30, command=lambda: mostrar_frame("equipo")).pack(pady=10)

# ==== MENÚ ROLES ====
def crear_menu_roles():
    frame = tk.Frame(contenedor)
    frames["roles"] = frame

    tk.Label(frame, text="Menú Roles", font=("Helvetica", 16)).pack(pady=10)

    #Agregar rol
    def mostrar_formulario_agregar_rol():
        roles.cargar_datos_roles()

        ventana = Toplevel()
        ventana.title("Agregar Rol")
        ventana.geometry("300x170")

        tk.Label(ventana, text="Nombre del nuevo rol:").pack(pady=5)
        entrada = tk.Entry(ventana)
        entrada.pack()

        mensaje = tk.Label(ventana, text="", fg="green")
        mensaje.pack(pady=5)

        def agregar():
            nombre = entrada.get().strip()
            if not nombre:
                mensaje.config(text="Ingresá un nombre.", fg="red")
                return
            if roles.agregar_rol(nombre):
                mensaje.config(text="Rol agregado correctamente.", fg="green")
                entrada.delete(0, tk.END)
            else:
                mensaje.config(text="Rol duplicado o inválido.", fg="red")
        tk.Button(ventana, text="Agregar", command=agregar).pack(pady=10)
    tk.Button(frame, text="Agregar nuevo rol", width=30, command=mostrar_formulario_agregar_rol).pack(pady=2)
    
    # Ver roles disponibles
    def mostrar_lista_roles():
        roles.cargar_datos_roles()
        if not roles.roles:
            messagebox.showinfo("Sin roles", "No hay roles registrados.")
            return

        ventana = Toplevel()
        ventana.title("Roles disponibles")
        ventana.geometry("300x250")

        tk.Label(ventana, text="Lista de roles:", font=("Helvetica", 12)).pack(pady=8)

        area = tk.Text(ventana, width=30, height=10)
        area.pack(padx=10)
        for rol in roles.roles:
            area.insert(tk.END, f"- {rol}\n")
        area.config(state=tk.DISABLED)
    tk.Button(frame, text="Ver roles disponibles", width=30, command=mostrar_lista_roles).pack(pady=2)

    # Eliminar rol
    def mostrar_formulario_eliminar_rol():
        roles.cargar_datos_roles()
        if not roles.roles:
            messagebox.showinfo("Sin roles", "No hay roles para eliminar.")
            return

        ventana = Toplevel()
        ventana.title("Eliminar Rol")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Seleccioná un rol:").pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly")
        combo["values"] = roles.roles
        combo.pack(pady=5)

        mensaje = tk.Label(ventana, text="", fg="red")
        mensaje.pack(pady=5)

        def eliminar():
            nombre = seleccion.get()
            if not nombre:
                mensaje.config(text="Seleccioná un rol.", fg="red")
                return
            if roles.eliminar_rol(nombre):
                mensaje.config(text="Rol eliminado correctamente.", fg="green")
                combo["values"] = roles.roles
                combo.set("")
            else:
                mensaje.config(text="No se pudo eliminar.", fg="red")

        tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=10)
    tk.Button(frame, text="Eliminar rol", width=30, command=mostrar_formulario_eliminar_rol).pack(pady=2)

    tk.Label(frame, text="").pack(pady=5)
    tk.Button(frame, text="Volver al Menú Equipo", width=30, command=lambda: mostrar_frame("equipo")).pack(pady=2)
    tk.Button(frame, text="Volver al Menú Principal", width=30, command=lambda: mostrar_frame("principal")).pack(pady=2)

# ==== Crear todos los menús ====
if __name__ == "__main__":
    equipo.cargar_datos_equipo()
    roles.cargar_datos_roles()
    tareas.cargar_datos_tareas()

    crear_menu_principal()
    crear_menu_equipo()
    crear_menu_supervisores()
    crear_menu_miembros()
    crear_menu_roles()
    crear_menu_tareas()

    mostrar_frame("principal")
    ventana.mainloop()