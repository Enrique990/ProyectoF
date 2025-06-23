import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import equipo

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

    tk.Label(frame, text="Menú Equipo", font=("Helvetica", 16)).pack(pady=10)

    # Crear Supervisor
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

    tk.Button(frame, text="Crear nuevo supervisor", width=25, command=mostrar_formulario_supervisor).pack(pady=3)

    # Agregar miembro
    def mostrar_formulario_miembro():
        equipo.cargar_datos_equipo()
        print(equipo.supervisores)
        if not equipo.supervisores:
            tk.messagebox.showwarning("Sin supervisores", "Primero debés crear un supervisor.")
            return

        ventana_miembro = Toplevel()
        ventana_miembro.title("Agregar Miembro")
        ventana_miembro.geometry("300x250")

        tk.Label(ventana_miembro, text="Supervisor:").pack(pady=2)
        entrada_supervisor = tk.Entry(ventana_miembro)
        entrada_supervisor.pack()

        tk.Label(ventana_miembro, text="Nombre del miembro:").pack(pady=2)
        entrada_nombre = tk.Entry(ventana_miembro)
        entrada_nombre.pack()

        tk.Label(ventana_miembro, text="Rol:").pack(pady=2)
        entrada_rol = tk.Entry(ventana_miembro)
        entrada_rol.pack()

        mensaje = tk.Label(ventana_miembro, text="", fg="green")
        mensaje.pack(pady=5)

        def procesar_agregado():
            sup = entrada_supervisor.get().strip()
            nombre = entrada_nombre.get().strip()
            rol = entrada_rol.get().strip()

            if not sup or not nombre or not rol:
                mensaje.config(text="Completa todos los campos.", fg="red")
                return

            exito = equipo.agregar_miembro(sup, nombre, rol)
            if exito:
                mensaje.config(text="Miembro agregado correctamente.", fg="green")
                entrada_supervisor.delete(0, tk.END)
                entrada_nombre.delete(0, tk.END)
                entrada_rol.delete(0, tk.END)
            else:
                mensaje.config(text="Nombre duplicado o supervisor no encontrado.", fg="red")


        tk.Button(ventana_miembro, text="Agregar", command=procesar_agregado).pack(pady=10)

    tk.Button(frame, text="Agregar miembro", width=25, command=mostrar_formulario_miembro).pack(pady=3)

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
    tk.Button(frame, text="Modificar miembro", width=25, command=lambda: print("Modificar miembro")).pack(pady=3)
    tk.Button(frame, text="Eliminar miembro", width=25, command=lambda: print("Eliminar miembro")).pack(pady=3)
    tk.Button(frame, text="Gestión de roles", width=25, command=lambda: mostrar_frame("roles")).pack(pady=3)
    tk.Button(frame, text="Volver al Menú Principal", width=25, command=lambda: mostrar_frame("principal")).pack(pady=10)


# ==== MENÚ TAREAS ====
def crear_menu_tareas():
    frame = tk.Frame(contenedor)
    frames["tareas"] = frame

    tk.Label(frame, text="Menú Tareas", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(frame, text="Agregar tarea a la cola", width=30, command=lambda: print("Agregar tarea")).pack(pady=2)
    tk.Button(frame, text="Ver cola de tareas", width=30, command=lambda: print("Ver tareas sin asignar")).pack(pady=2)
    tk.Button(frame, text="Modificar una tarea", width=30, command=lambda: print("Modificar tarea")).pack(pady=2)
    tk.Button(frame, text="Eliminar una tarea", width=30, command=lambda: print("Eliminar tarea")).pack(pady=2)
    tk.Button(frame, text="Asignar tareas automáticamente", width=30, command=lambda: print("Asignar automáticamente")).pack(pady=2)
    tk.Button(frame, text="Ver tareas asignadas por persona", width=30, command=lambda: print("Ver tareas por persona")).pack(pady=2)
    tk.Button(frame, text="Exportar informe", width=30, command=lambda: print("Exportar a Excel")).pack(pady=2)
    tk.Button(frame, text="Volver al Menú Principal", width=30, command=lambda: mostrar_frame("principal")).pack(pady=10)

# ==== MENÚ ROLES ====
def crear_menu_roles():
    frame = tk.Frame(contenedor)
    frames["roles"] = frame

    tk.Label(frame, text="Menú Roles", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(frame, text="Agregar nuevo rol", width=30, command=lambda: print("Agregar rol")).pack(pady=2)
    tk.Button(frame, text="Ver roles disponibles", width=30, command=lambda: print("Ver roles")).pack(pady=2)
    tk.Button(frame, text="Eliminar rol", width=30, command=lambda: print("Eliminar rol")).pack(pady=2)
    tk.Label(frame, text="").pack(pady=5)
    tk.Button(frame, text="Volver al Menú Equipo", width=30, command=lambda: mostrar_frame("equipo")).pack(pady=2)
    tk.Button(frame, text="Volver al Menú Principal", width=30, command=lambda: mostrar_frame("principal")).pack(pady=2)

# ==== Crear todos los menús ====
crear_menu_principal()
crear_menu_equipo()
crear_menu_tareas()
crear_menu_roles()
mostrar_frame("principal")

ventana.mainloop()