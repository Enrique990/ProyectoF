import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, END, Listbox, Text, Scrollbar, RIGHT, Y, END
import equipo, roles, tareas, json, os
from modelos import Equipo, Supervisor
from excel_export import exportar_tareas_a_excel
from tkinter.ttk import Combobox

# Configuración de estilo global
DARK_BG = "#2d2d2d"
DARK_FG = "#e0e0e0"
ACCENT_COLOR = "#4a9cff"
HOVER_COLOR = "#3a7bc8"
BUTTON_BG = "#3a3a3a"
TEXT_BG = "#383838"
ENTRY_BG = "#454545"
FONT_FAMILY = "Segoe UI"  # Fuente moderna (se usará Arial como fallback)
BASE_FONT_SIZE = 10
current_font_size = BASE_FONT_SIZE

# Cargar supervisor desde archivo JSON
with open("datos/equipo.json", "r", encoding="utf-8") as archivo:
    supervisor_raw = json.load(archivo)
    equipos = [Supervisor.from_dict(d) for d in supervisor_raw]

# ==== Ventana principal ====
ventana = tk.Tk()
ventana.title("TaskTree - Menú Principal")
ventana.geometry("500x500")
ventana.configure(bg=DARK_BG)

# Configurar estilo ttk
style = ttk.Style()
style.theme_use('clam')

# Configuraciones de estilo
style.configure('TFrame', background=DARK_BG)
style.configure('TLabel', background=DARK_BG, foreground=DARK_FG, font=(FONT_FAMILY, current_font_size))
style.configure('TButton', background=BUTTON_BG, foreground=DARK_FG, font=(FONT_FAMILY, current_font_size), 
                borderwidth=1, relief="flat")
style.map('TButton', background=[('active', HOVER_COLOR)], foreground=[('active', 'white')])
style.configure('TCombobox', fieldbackground=ENTRY_BG, background=ENTRY_BG, foreground=DARK_FG, 
                selectbackground=ACCENT_COLOR, selectforeground='white')
style.configure('TEntry', fieldbackground=ENTRY_BG, foreground=DARK_FG)
style.configure('Treeview', background=TEXT_BG, foreground=DARK_FG, fieldbackground=TEXT_BG, 
                font=(FONT_FAMILY, current_font_size))
style.map('Treeview', background=[('selected', ACCENT_COLOR)], foreground=[('selected', 'white')])
style.configure('Vertical.TScrollbar', background=BUTTON_BG, troughcolor=DARK_BG)

# Contenedor principal
contenedor = tk.Frame(ventana, bg=DARK_BG)
contenedor.pack(fill="both", expand=True, padx=10, pady=10)

# Barra de control de tamaño de fuente
font_control_frame = tk.Frame(ventana, bg=DARK_BG)
font_control_frame.pack(side="bottom", fill="x", padx=10, pady=5)

tk.Label(font_control_frame, text="Tamaño de texto:", bg=DARK_BG, fg=DARK_FG, 
         font=(FONT_FAMILY, current_font_size)).pack(side="left", padx=5)

def increase_font():
    global current_font_size
    if current_font_size < 16:
        current_font_size += 1
        update_fonts()
        ventana.update()  # Forzar actualización de la interfaz

def decrease_font():
    global current_font_size
    if current_font_size > 8:
        current_font_size -= 1
        update_fonts()
        ventana.update()  # Forzar actualización de la interfaz

def update_fonts():
    # Actualizar estilos ttk
    style.configure('TLabel', font=(FONT_FAMILY, current_font_size))
    style.configure('TButton', font=(FONT_FAMILY, current_font_size))
    style.configure('Treeview', font=(FONT_FAMILY, current_font_size))
    style.configure('TCombobox', font=(FONT_FAMILY, current_font_size))
    style.configure('TEntry', font=(FONT_FAMILY, current_font_size))
    
    # Función recursiva para actualizar todos los widgets
    def update_widgets(window):
        for widget in window.winfo_children():
            try:
                # Widgets estándar
                if isinstance(widget, (tk.Label, tk.Button, tk.Listbox, tk.Entry, tk.Text, tk.Checkbutton, tk.Radiobutton)):
                    widget.config(font=(FONT_FAMILY, current_font_size))
                
                # Widgets ttk
                elif isinstance(widget, (ttk.Label, ttk.Button, ttk.Combobox, ttk.Entry, ttk.Treeview)):
                    style.configure(widget.winfo_class(), font=(FONT_FAMILY, current_font_size))
                    widget.config(style=widget.winfo_class())
                
                # Actualizar widgets hijos
                if hasattr(widget, 'winfo_children'):
                    update_widgets(widget)
            except:
                continue
    
    # Actualizar ventana principal y todas las secundarias
    update_widgets(ventana)
    for window in ventana.winfo_children():
        if isinstance(window, tk.Toplevel):
            update_widgets(window)

tk.Button(font_control_frame, text="A+", command=increase_font, bg=BUTTON_BG, fg=DARK_FG, 
          font=(FONT_FAMILY, current_font_size), relief="flat", borderwidth=0).pack(side="left", padx=2)
tk.Button(font_control_frame, text="A-", command=decrease_font, bg=BUTTON_BG, fg=DARK_FG, 
          font=(FONT_FAMILY, current_font_size), relief="flat", borderwidth=0).pack(side="left", padx=2)

# Diccionario de frames
frames = {}

# ==== Función para mostrar cualquier menú ====
def mostrar_frame(nombre):
    for f in frames.values():
        f.pack_forget()
    frames[nombre].pack(fill="both", expand=True, padx=10, pady=10)

# ==== MENÚ PRINCIPAL ====
def crear_menu_principal():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["principal"] = frame

    tk.Label(frame, text="Menú Principal", font=(FONT_FAMILY, current_font_size+4, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=20)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

    tk.Button(frame, text="Menú Equipo", width=30, command=lambda: mostrar_frame("equipo"), **button_style).pack(pady=8)
    tk.Button(frame, text="Menú Tareas", width=30, command=lambda: mostrar_frame("tareas"), **button_style).pack(pady=8)
    tk.Button(frame, text="Menú Roles", width=30, command=lambda: mostrar_frame("roles"), **button_style).pack(pady=8)
    tk.Button(frame, text="Salir", width=30, command=ventana.destroy, **button_style).pack(pady=20)

# ==== MENÚ EQUIPO ====
def crear_menu_equipo():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["equipo"] = frame

    tk.Label(frame, text="Gestión de Equipo", font=(FONT_FAMILY, current_font_size+2, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

    # Mostrar estructura
    def mostrar_estructura_equipo():
        equipo.cargar_datos_equipo()
        ventana_arbol = Toplevel()
        ventana_arbol.title("Estructura del Equipo")
        ventana_arbol.geometry("500x400")
        ventana_arbol.configure(bg=DARK_BG)

        tree = ttk.Treeview(ventana_arbol)
        tree.heading("#0", text="Estructura", anchor="w")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for s in equipo.supervisores:
            id_sup = tree.insert("", "end", text=f"Supervisor: {s.nombre}")

            if s.equipo:
                id_eq = tree.insert(id_sup, "end", text=f"Equipo: {s.equipo.nombre}")

                total_tareas = 0  # acumulador de tareas del equipo

                for m in s.equipo.miembros:
                    cantidad = len(m.tareas)
                    total_tareas += cantidad
                    tree.insert(id_eq, "end", text=f"{m.nombre} (rol: {m.rol}, tareas: {cantidad})")

                # Mostrar total de tareas del equipo justo debajo
                tree.insert(id_eq, "end", text=f"Total de tareas asignadas al supervisor: {total_tareas}")

    tk.Button(frame, text="Menú Supervisores", width=25, command=lambda: mostrar_frame("supervisores"), **button_style).pack(pady=5)
    tk.Button(frame, text="Menú Miembros", width=25, command=lambda: mostrar_frame("miembros"), **button_style).pack(pady=5)
    tk.Button(frame, text="Ver estructura del equipo", width=25, command=mostrar_estructura_equipo, **button_style).pack(pady=5)
    tk.Button(frame, text="Gestión de roles", width=25, command=lambda: mostrar_frame("roles"), **button_style).pack(pady=5)
    tk.Button(frame, text="Volver al Menú Principal", width=25, command=lambda: mostrar_frame("principal"), **button_style).pack(pady=15)

# ==== MENÚ VER TAREAS ====
def crear_menu_ver_tareas():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["ver_tareas"] = frame

    tk.Label(frame, text="Menú Ver Tareas", font=(FONT_FAMILY, current_font_size+2, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

    # Ver tareas asignadas por persona
    def mostrar_tareas_por_persona():
        equipo.cargar_datos_equipo()
        tareas.cargar_datos_tareas()
        roles.cargar_datos_roles()
        sincronizar_tareas_en_equipo()
        ventana = Toplevel()
        ventana.title("Tareas por Persona")
        ventana.geometry("500x400")
        ventana.configure(bg=DARK_BG)
        
        nombres = [p.nombre for sup in equipo.supervisores for p in sup.equipo.miembros]
        
        tk.Label(ventana, text="Seleccione una persona:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        combo = Combobox(ventana, values=nombres, state="readonly")
        combo.pack(padx=10, pady=5)
        
        tk.Label(ventana, text="Tareas asignadas:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        listbox = Listbox(ventana, width=50, height=15, bg=TEXT_BG, fg=DARK_FG, selectbackground=ACCENT_COLOR)
        listbox.pack(padx=10, pady=5, fill="both", expand=True)
        
        scrollbar = Scrollbar(ventana, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        
        def on_select(event):
            seleccionado = combo.get()
            listbox.delete(0, END)
            for sup in equipo.supervisores:
                for persona in sup.equipo.miembros:
                    if persona.nombre == seleccionado:
                        for tarea in persona.tareas:
                            listbox.insert(END, tarea)
                        return
        combo.bind("<<ComboboxSelected>>", on_select)

    tk.Button(frame, text="Tareas por miembro", width=30,
          command=lambda: mostrar_tareas_por_persona() if hay_miembros() and hay_tareas_asignadas()
          else messagebox.showinfo("Sin datos", "Debe haber al menos un miembro y una tarea asignada."),
          **button_style).pack(pady=5)

    # Ver tareas por rol
    def mostrar_tareas_por_rol():
        tareas.cargar_datos_tareas()
        roles.cargar_datos_roles()
        sincronizar_tareas_en_equipo()

        ventana = Toplevel()
        ventana.title("Tareas por Rol")
        ventana.geometry("500x400")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná un rol:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        roles_disponibles = list({t["rol"] for t in tareas.tareas if "rol" in t})
        combo = ttk.Combobox(ventana, values=roles_disponibles, state="readonly")
        combo.pack(pady=5)

        tk.Label(ventana, text="Tareas:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        listbox = tk.Listbox(ventana, width=60, height=15, bg=TEXT_BG, fg=DARK_FG, selectbackground=ACCENT_COLOR)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = Scrollbar(ventana, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def on_select(event):
            listbox.delete(0, tk.END)
            rol_seleccionado = combo.get()
            for t in tareas.tareas:
                if t.get("rol") == rol_seleccionado:
                    estado = t.get("estado", "desconocido")
                    asignada = "✅" if t.get("asignada") else "❌"
                    miembro = t.get("miembro", "Sin asignar")
                    listbox.insert(tk.END, f"{t['nombre']} ({estado}, {miembro}, asignada: {asignada})")

        combo.bind("<<ComboboxSelected>>", on_select)

    tk.Button(frame, text="Tareas por rol", width=30,
          command=lambda: mostrar_tareas_por_rol() if hay_tareas()
          else messagebox.showinfo("Sin tareas", "No hay tareas disponibles."),
          **button_style).pack(pady=5)

    # Ver tareas por prioridad
    def mostrar_tareas_por_prioridad():
        tareas.cargar_datos_tareas()
        sincronizar_tareas_en_equipo()

        ventana = Toplevel()
        ventana.title("Tareas por Prioridad")
        ventana.geometry("500x400")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná una prioridad:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        prioridades = list({t.get("prioridad", "Sin prioridad") for t in tareas.tareas})
        combo = ttk.Combobox(ventana, values=prioridades, state="readonly")
        combo.pack(pady=5)

        tk.Label(ventana, text="Tareas:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        listbox = tk.Listbox(ventana, width=60, height=15, bg=TEXT_BG, fg=DARK_FG, selectbackground=ACCENT_COLOR)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = Scrollbar(ventana, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def on_select(event):
            listbox.delete(0, tk.END)
            prioridad = combo.get()
            for t in tareas.tareas:
                if t.get("prioridad") == prioridad:
                    estado = t.get("estado", "desconocido")
                    miembro = t.get("miembro", "Sin asignar")
                    asignada = "✅" if t.get("asignada") else "❌"
                    listbox.insert(tk.END, f"{t['nombre']} ({estado}, {miembro}, asignada: {asignada})")

        combo.bind("<<ComboboxSelected>>", on_select)

    tk.Button(frame, text="Tareas por prioridad", width=30,
          command=lambda: mostrar_tareas_por_prioridad() if hay_tareas()
          else messagebox.showinfo("Sin tareas", "No hay tareas disponibles."),
          **button_style).pack(pady=5)

    # Ver tareas por estado
    def mostrar_tareas_por_estado():
        tareas.cargar_datos_tareas()
        sincronizar_tareas_en_equipo()

        ventana = Toplevel()
        ventana.title("Tareas por Estado")
        ventana.geometry("500x400")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná un estado:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        estados = list({t.get("estado", "Sin estado") for t in tareas.tareas})
        combo = ttk.Combobox(ventana, values=estados, state="readonly")
        combo.pack(pady=5)

        tk.Label(ventana, text="Tareas:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        listbox = tk.Listbox(ventana, width=60, height=15, bg=TEXT_BG, fg=DARK_FG, selectbackground=ACCENT_COLOR)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = Scrollbar(ventana, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def on_select(event):
            listbox.delete(0, tk.END)
            estado = combo.get()
            for t in tareas.tareas:
                if t.get("estado") == estado:
                    prioridad = t.get("prioridad", "Sin prioridad")
                    miembro = t.get("miembro", "Sin asignar")
                    asignada = "✅" if t.get("asignada") else "❌"
                    listbox.insert(tk.END, f"{t['nombre']} ({prioridad}, {miembro}, asignada: {asignada})")

        combo.bind("<<ComboboxSelected>>", on_select)

    tk.Button(frame, text="Tareas por estado", width=30,
          command=lambda: mostrar_tareas_por_estado() if hay_tareas()
          else messagebox.showinfo("Sin tareas", "No hay tareas disponibles."),
          **button_style).pack(pady=5)

    # Ver tareas por equipo
    def mostrar_tareas_por_equipo():
        equipo.cargar_datos_equipo()
        tareas.cargar_datos_tareas()
        sincronizar_tareas_en_equipo()

        ventana = Toplevel()
        ventana.title("Tareas por Equipo")
        ventana.geometry("500x400")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná un equipo:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        nombres_equipos = [sup.equipo.nombre for sup in equipo.supervisores if sup.equipo]
        combo = ttk.Combobox(ventana, values=nombres_equipos, state="readonly")
        combo.pack(pady=5)

        tk.Label(ventana, text="Tareas:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        listbox = tk.Listbox(ventana, width=60, height=15, bg=TEXT_BG, fg=DARK_FG, selectbackground=ACCENT_COLOR)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = Scrollbar(ventana, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def on_select(event):
            listbox.delete(0, tk.END)
            nombre_equipo = combo.get()

            for sup in equipo.supervisores:
                if sup.equipo and sup.equipo.nombre == nombre_equipo:
                    for persona in sup.equipo.miembros:
                        for t in tareas.tareas:
                            if t.get("miembro") == persona.nombre:
                                estado = t.get("estado", "desconocido")
                                asignada = "✅" if t.get("asignada") else "❌"
                                listbox.insert(tk.END, f"{t['nombre']} ({estado}, {persona.nombre}, asignada: {asignada})")
                    return

        combo.bind("<<ComboboxSelected>>", on_select)

    tk.Button(frame, text="Tareas por equipo/supervisor", width=30,
          command=lambda: mostrar_tareas_por_equipo() if hay_tareas_asignadas()
          else messagebox.showinfo("Sin tareas asignadas", "No hay tareas asignadas."),
          **button_style).pack(pady=5)

    # Ver tareas asignadas
    def mostrar_tareas_asignadas():
        tareas.cargar_datos_tareas()
        sincronizar_tareas_en_equipo()

        ventana = Toplevel()
        ventana.title("Tareas Asignadas")
        ventana.geometry("500x400")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Tareas actualmente asignadas:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        listbox = tk.Listbox(ventana, width=70, height=20, bg=TEXT_BG, fg=DARK_FG, selectbackground=ACCENT_COLOR)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar = Scrollbar(ventana, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        tareas_asignadas = [t for t in tareas.tareas if t.get("asignada")]

        if not tareas_asignadas:
            listbox.insert(tk.END, "No hay tareas asignadas.")
        else:
            for t in tareas_asignadas:
                estado = t.get("estado", "desconocido")
                miembro = t.get("miembro", "Sin asignar")
                rol = t.get("rol", "Sin rol")
                listbox.insert(tk.END, f"{t['nombre']} ({estado}, {miembro}, rol: {rol})")

    tk.Button(frame, text="Tareas asignadas", width=30,
          command=lambda: mostrar_tareas_asignadas() if hay_tareas_asignadas()
          else messagebox.showinfo("Sin tareas asignadas", "No hay tareas asignadas."),
          **button_style).pack(pady=5)

    # Ver cola de tareas sin asignar
    def mostrar_cola_tareas():
        tareas.cargar_datos_tareas()
        sincronizar_tareas_en_equipo()
        tareas_no_asignadas = [t for t in tareas.tareas if not t["asignada"]]

        if not tareas_no_asignadas:
            messagebox.showinfo("Sin tareas", "La cola de tareas está vacía.")
            return

        ventana = Toplevel()
        ventana.title("Cola de Tareas")
        ventana.geometry("600x400")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Tareas sin asignar", font=("Helvetica", 12), bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        text_frame = tk.Frame(ventana, bg=DARK_BG)
        text_frame.pack(padx=10, pady=5, fill="both", expand=True)

        area = tk.Text(text_frame, width=70, height=20, bg=TEXT_BG, fg=DARK_FG, wrap="word")
        area.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(text_frame, command=area.yview)
        scrollbar.pack(side="right", fill="y")
        area.config(yscrollcommand=scrollbar.set)

        for t in tareas_no_asignadas:
            area.insert(tk.END,
                f"- {t['nombre']}\n"
                f"  Prioridad: {t['prioridad']} | Estado: {t['estado']} | Rol requerido: {t['rol']}\n"
                f"  Descripción: {t['descripcion']}\n\n"
            )
        area.config(state=tk.DISABLED)

    tk.Button(frame, text="Cola de tareas sin asignar", width=30, command=mostrar_cola_tareas, **button_style).pack(pady=5)

    # Historial de tareas eliminadas
    def mostrar_historial_tareas_eliminadas():
        ruta = "datos/historial.json"

        if not os.path.exists(ruta):
            messagebox.showinfo("Historial vacío", "Aún no hay tareas eliminadas registradas.")
            return

        with open(ruta, "r", encoding="utf-8") as archivo:
            historial = json.load(archivo)

        ventana = Toplevel()
        ventana.title("Historial de Tareas Eliminadas")
        ventana.geometry("700x500")
        ventana.configure(bg=DARK_BG)

        text_frame = tk.Frame(ventana, bg=DARK_BG)
        text_frame.pack(padx=10, pady=10, fill="both", expand=True)

        area = Text(text_frame, wrap="word", bg=TEXT_BG, fg=DARK_FG)
        area.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(text_frame, command=area.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        area.config(yscrollcommand=scrollbar.set)

        if not historial:
            area.insert(END, "No hay tareas eliminadas registradas.")
        else:
            for t in historial:
                area.insert(END, f"🗑️ {t['nombre']} (Rol: {t.get('rol', '-')}, Miembro: {t.get('miembro', '-')})\n")
                area.insert(END, f"   Prioridad: {t.get('prioridad', '-')}\n")
                area.insert(END, f"   Descripción: {t.get('descripcion', '-')}\n")
                area.insert(END, f"   Fecha de eliminación: {t.get('fecha_eliminacion', '-')}\n\n")
        area.config(state="disabled")

    tk.Button(frame, text="Historial de tareas eliminadas", width=30, command=mostrar_historial_tareas_eliminadas, **button_style).pack(pady=5)

    tk.Button(frame, text="Volver a menú tareas", width=30, command=lambda: mostrar_frame("tareas"), **button_style).pack(pady=15)

# ==== MENÚ TAREAS ====
def crear_menu_tareas():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["tareas"] = frame

    tk.Label(frame, text="Menú Tareas", font=(FONT_FAMILY, current_font_size+2, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

    # Agregar tarea a la cola
    def mostrar_formulario_agregar_tarea():
        tareas.cargar_datos_tareas()
        roles.cargar_datos_roles()

        ventana = Toplevel()
        ventana.title("Agregar Tarea a la Cola")
        ventana.geometry("350x450")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Nombre de la tarea:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        entrada = tk.Entry(ventana, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        entrada.pack()

        tk.Label(ventana, text="Descripción:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        texto = tk.Text(ventana, height=6, width=30, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        texto.pack()

        tk.Label(ventana, text="Rol requerido:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        rol_var = tk.StringVar()
        combo_rol = ttk.Combobox(ventana, textvariable=rol_var, state="readonly")
        combo_rol["values"] = roles.roles
        combo_rol.pack()

        tk.Label(ventana, text="Prioridad:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        prioridad_var = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=prioridad_var, state="readonly")
        combo["values"] = ["Alta", "Media", "Baja"]
        combo.pack()

        mensaje = tk.Label(ventana, text="", fg="green", bg=DARK_BG)
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
                combo_rol.set("")
                combo.set("")
                texto.delete("1.0", tk.END)
            else:
                mensaje.config(text="Nombre inválido o duplicado.", fg="red")

        tk.Button(ventana, text="Agregar", command=agregar, **button_style).pack(pady=10)

    tk.Button(frame, text="Agregar tarea a la cola", width=30, command=mostrar_formulario_agregar_tarea, **button_style).pack(pady=5)
    
    # Ver tareas 
    tk.Button(frame, text="Ver tareas (menú)", width=30, command=lambda: mostrar_frame("ver_tareas"), **button_style).pack(pady=5)
    
    # Eliminar tarea
    def mostrar_formulario_eliminar_tarea():
        tareas.cargar_datos_tareas()
        lista_tareas = tareas.tareas.copy()

        if not lista_tareas:
            messagebox.showinfo("Sin tareas", "No hay tareas para eliminar.")
            return

        ventana = Toplevel()
        ventana.title("Eliminar Tarea")
        ventana.geometry("450x300")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná una tarea a eliminar:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)

        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly", width=45)

        def descripcion_tarea(t):
            asignada = f"Asignada a {t['miembro']}" if t["asignada"] else "Sin asignar"
            return f"{t['nombre']} ({asignada})"

        opciones = [descripcion_tarea(t) for t in lista_tareas]
        combo["values"] = opciones
        combo.pack(pady=5)

        mensaje = tk.Label(ventana, text="", fg="red", bg=DARK_BG)
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
                        tareas.guardar_en_historial(t)
                        tareas.tareas.remove(t)
                        tareas.guardar_datos_tareas()
                        tareas.cargar_datos_tareas()
                        roles.cargar_datos_roles()
                        sincronizar_tareas_en_equipo()
                        mensaje.config(text="Tarea eliminada con éxito.", fg="green")
                        combo["values"] = [descripcion_tarea(t) for t in tareas.tareas]
                        combo.set("")
                    return

            mensaje.config(text="No se pudo eliminar la tarea.", fg="red")

        tk.Button(ventana, text="Eliminar", command=eliminar, **button_style).pack(pady=10)

    tk.Button(frame, text="Eliminar una tarea", width=30, command=mostrar_formulario_eliminar_tarea, **button_style).pack(pady=5)
    
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
        ventana.geometry("400x450")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná una tarea:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly", width=35)
        combo["values"] = [t["nombre"] for t in tareas_pendientes]
        combo.pack(pady=5)

        tk.Label(ventana, text="Nuevo nombre:", bg=DARK_BG, fg=DARK_FG).pack()
        entrada_nombre = tk.Entry(ventana, width=35, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        entrada_nombre.pack(pady=2)

        tk.Label(ventana, text="Nuevo rol requerido:", bg=DARK_BG, fg=DARK_FG).pack()
        rol_var = tk.StringVar()
        combo_rol = ttk.Combobox(ventana, textvariable=rol_var, state="readonly")
        combo_rol["values"] = roles.roles
        combo_rol.pack(pady=2)

        tk.Label(ventana, text="Nueva prioridad:", bg=DARK_BG, fg=DARK_FG).pack()
        prioridad_var = tk.StringVar()
        combo_prioridad = ttk.Combobox(ventana, textvariable=prioridad_var, state="readonly")
        combo_prioridad["values"] = ["Alta", "Media", "Baja"]
        combo_prioridad.pack(pady=2)

        tk.Label(ventana, text="Nueva descripción:", bg=DARK_BG, fg=DARK_FG).pack()
        texto = tk.Text(ventana, height=6, width=35, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        texto.pack(pady=2)

        mensaje = tk.Label(ventana, text="", fg="red", bg=DARK_BG)
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
                    combo_rol.set("")
                    combo_prioridad.set("")
                    texto.delete("1.0", tk.END)
                    return

            mensaje.config(text="No se pudo modificar la tarea.", fg="red")

        tk.Button(ventana, text="Guardar cambios", command=modificar, **button_style).pack(pady=10)

    tk.Button(frame, text="Modificar tarea sin asignar", width=30, command=mostrar_modificar_tarea_no_asignada, **button_style).pack(pady=5)
    
    # Modificar tarea asignada
    def mostrar_modificar_tarea_asignada():
        tareas.cargar_datos_tareas()
        nombres_miembros = [p.nombre for sup in equipo.supervisores for p in sup.equipo.miembros]
        tareas_asignadas = [t for t in tareas.tareas if t["asignada"]]

        if not tareas_asignadas:
            messagebox.showinfo("Sin tareas", "No hay tareas asignadas para modificar.")
            return

        ventana = Toplevel()
        ventana.title("Modificar Tarea Asignada")
        ventana.geometry("400x300")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná una tarea asignada:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly", width=35)
        combo["values"] = [f"{t['nombre']} ({t['miembro']})" for t in tareas_asignadas]
        combo.pack(pady=5)

        tk.Label(ventana, text="Nuevo estado:", bg=DARK_BG, fg=DARK_FG).pack()
        estado_var = tk.StringVar()
        combo_estado = ttk.Combobox(ventana, textvariable=estado_var, state="readonly")
        combo_estado["values"] = ["pendiente", "en proceso", "finalizada"]
        combo_estado.pack(pady=5)

        tk.Label(ventana, text="Nuevo responsable:", bg=DARK_BG, fg=DARK_FG).pack()
        miembro_var = tk.StringVar()
        combo_miembro = ttk.Combobox(ventana, textvariable=miembro_var, state="readonly")
        combo_miembro["values"] = nombres_miembros
        combo_miembro.pack(pady=5)

        mensaje = tk.Label(ventana, text="", fg="green", bg=DARK_BG)
        mensaje.pack(pady=5)

        def actualizar_miembros_disponibles(event):
            seleccion_texto = seleccion.get()
            if not seleccion_texto:
                return
        
            nombre_tarea = seleccion_texto.split(" (")[0]
            tarea = next((t for t in tareas.tareas if t["nombre"] == nombre_tarea), None)
            if not tarea:
                return
        
            rol_requerido = tarea.get("rol")
            miembros_validos = [
                p.nombre
                for sup in equipo.supervisores
                for p in sup.equipo.miembros
                if p.rol == rol_requerido
            ]
        
            combo_miembro["values"] = miembros_validos
            combo_miembro.set("")  # limpiar selección anterior

        combo.bind("<<ComboboxSelected>>", actualizar_miembros_disponibles)

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
                            tareas.guardar_en_historial(t)
                            tareas.tareas.remove(t)
                            tareas.guardar_datos_tareas()
                            sincronizar_tareas_en_equipo()
                            tareas.cargar_datos_tareas()
                            roles.cargar_datos_roles()
                            mensaje.config(text="Tarea finalizada y eliminada.", fg="green")
                            combo["values"] = [f"{t['nombre']} ({t['miembro']})" for t in tareas.tareas if t["asignada"]]
                            combo.set("")
                            combo_estado.set("")
                            combo_miembro.set("")
                        return
                    else:
                        t["estado"] = nuevo_estado
                        nuevo_miembro = miembro_var.get()
                        if nuevo_miembro:
                            t["miembro"] = nuevo_miembro
                        tareas.guardar_datos_tareas()
                        mensaje.config(text="Tarea actualizada exitosamente.", fg="green")
                        combo["values"] = [f"{t['nombre']} ({t['miembro']})" for t in tareas.tareas if t["asignada"]]
                        combo.set("")
                        combo_estado.set("")
                        combo_miembro.set("")
                        sincronizar_tareas_en_equipo()
                        return

            mensaje.config(text="No se pudo modificar la tarea.", fg="red")

        tk.Button(ventana, text="Guardar cambios", command=modificar_estado, **button_style).pack(pady=10)

    tk.Button(frame, text="Modificar tarea asignada", width=30, command=mostrar_modificar_tarea_asignada, **button_style).pack(pady=5)

    # Asignar tareas automáticamente
    def asignar_tareas_automaticamente():
        equipo.cargar_datos_equipo()
        miembros = equipo.obtener_todos_los_miembros(equipo.supervisores)

        if not miembros:
            messagebox.showinfo("Equipo vacío", "No hay miembros en el equipo.")
            return

        cantidad = tareas.asignar_tareas_por_rol_y_prioridad(miembros)

        if cantidad > 0:
            tareas.cargar_datos_tareas()
            equipo.cargar_datos_equipo()
            for sup in equipo.supervisores:
                for persona in sup.equipo.miembros:
                    persona.tareas.clear()
            for t in tareas.tareas:
                if t.get("asignada"):
                    for sup in equipo.supervisores:
                        for persona in sup.equipo.miembros:
                            if persona.nombre == t["miembro"]:
                                persona.asignar_tarea(t["nombre"])
            equipo.guardar_datos_equipo()
            messagebox.showinfo(
                "Asignación completa",
                f"Se asignaron {cantidad} tarea(s) automáticamente\n"
            )
        else:
            messagebox.showinfo("Sin asignaciones", "No hay tareas que se puedan asignar.")

    tk.Button(frame, text="Asignar tareas automáticamente", width=30, command=asignar_tareas_automaticamente, **button_style).pack(pady=5)
    
    # Exportar informe a Excel
    def exportar_tareas():
        tareas.cargar_datos_tareas()
        exito, resultado = exportar_tareas_a_excel(tareas.tareas)
        if exito:
            messagebox.showinfo("Exportación exitosa", f"Tareas exportadas a: {resultado}")
        else:
            messagebox.showinfo("Sin datos", resultado)

    tk.Button(frame, text="Exportar informe", width=30, command=exportar_tareas, **button_style).pack(pady=5)

    tk.Button(frame, text="Volver al Menú Principal", width=30, command=lambda: mostrar_frame("principal"), **button_style).pack(pady=15)

# ==== MENÚ SUPERVISOR ====
def crear_menu_supervisores():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["supervisores"] = frame

    tk.Label(frame, text="Menú Supervisores", font=(FONT_FAMILY, current_font_size+2, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

    # Crear nuevo supervisor
    def mostrar_formulario_supervisor():
        ventana_sup = Toplevel()
        ventana_sup.title("Crear Supervisor")
        ventana_sup.geometry("350x250")
        ventana_sup.configure(bg=DARK_BG)

        tk.Label(ventana_sup, text="Nombre del supervisor:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        entrada_sup = tk.Entry(ventana_sup, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        entrada_sup.pack()

        tk.Label(ventana_sup, text="Nombre del equipo:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        entrada_eq = tk.Entry(ventana_sup, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        entrada_eq.pack()

        mensaje = tk.Label(ventana_sup, text="", fg="green", bg=DARK_BG)
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

        tk.Button(ventana_sup, text="Crear", command=procesar_creacion, **button_style).pack(pady=10)

    tk.Button(frame, text="Crear nuevo supervisor", width=30, command=mostrar_formulario_supervisor, **button_style).pack(pady=5)

    # Listar supervisores
    def mostrar_lista_supervisores():
        equipo.cargar_datos_equipo()
        supervisores = equipo.supervisores

        if not supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores registrados.")
            return

        ventana_ver = Toplevel()
        ventana_ver.title("Supervisores Registrados")
        ventana_ver.geometry("400x300")
        ventana_ver.configure(bg=DARK_BG)

        tk.Label(ventana_ver, text="Lista de Supervisores", font=("Helvetica", 14), bg=DARK_BG, fg=DARK_FG).pack(pady=8)

        text_frame = tk.Frame(ventana_ver, bg=DARK_BG)
        text_frame.pack(padx=10, pady=5, fill="both", expand=True)

        texto = tk.Text(text_frame, width=40, height=10, bg=TEXT_BG, fg=DARK_FG)
        texto.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(text_frame, command=texto.yview)
        scrollbar.pack(side="right", fill="y")
        texto.config(yscrollcommand=scrollbar.set)

        for s in supervisores:
            nombre_eq = s.equipo.nombre if s.equipo else "Sin equipo"
            texto.insert(tk.END, f"Supervisor: {s.nombre}  →  Equipo: {nombre_eq}\n")

        texto.config(state=tk.DISABLED)

    tk.Button(frame, text="Ver supervisores", width=30, command=mostrar_lista_supervisores, **button_style).pack(pady=5)

    # Eliminar supervisor
    def mostrar_eliminacion_supervisor():
        equipo.cargar_datos_equipo()
        supervisores = equipo.supervisores
        if not supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores para eliminar.")
            return

        ventana_eliminar = Toplevel()
        ventana_eliminar.title("Eliminar Supervisor")
        ventana_eliminar.geometry("350x250")
        ventana_eliminar.configure(bg=DARK_BG)

        tk.Label(ventana_eliminar, text="Selecciona un supervisor:", bg=DARK_BG, fg=DARK_FG).pack(pady=3)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana_eliminar, textvariable=seleccion, state="readonly")
        combo["values"] = [s.nombre for s in supervisores]
        combo.pack(pady=5)

        mensaje = tk.Label(ventana_eliminar, text="", fg="red", bg=DARK_BG)
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

        tk.Button(ventana_eliminar, text="Eliminar", command=eliminar, **button_style).pack(pady=10)

    tk.Button(frame, text="Eliminar supervisor", width=30, command=mostrar_eliminacion_supervisor, **button_style).pack(pady=5)

    tk.Button(frame, text="Volver al menú Equipo", width=30, command=lambda: mostrar_frame("equipo"), **button_style).pack(pady=15)

# ==== MENÚ MIEMBROS ====
def crear_menu_miembros():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["miembros"] = frame

    tk.Label(frame, text="Menú Miembros", font=(FONT_FAMILY, current_font_size+2, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

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
        ventana_miembro.geometry("350x300")
        ventana_miembro.configure(bg=DARK_BG)

        tk.Label(ventana_miembro, text="Supervisor:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(ventana_miembro, textvariable=supervisor_var, state="readonly")
        supervisor_combo["values"] = [s.nombre for s in equipo.supervisores]
        supervisor_combo.pack()

        tk.Label(ventana_miembro, text="Nombre del miembro:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        entrada_nombre = tk.Entry(ventana_miembro, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        entrada_nombre.pack()

        tk.Label(ventana_miembro, text="Rol:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        rol_var = tk.StringVar()
        rol_combo = ttk.Combobox(ventana_miembro, textvariable=rol_var, state="readonly")
        rol_combo["values"] = roles.roles
        rol_combo.pack()

        mensaje = tk.Label(ventana_miembro, text="", fg="green", bg=DARK_BG)
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

        tk.Button(ventana_miembro, text="Agregar", command=procesar_agregado, **button_style).pack(pady=10)

    tk.Button(frame, text="Agregar miembro", width=30, command=mostrar_formulario_miembro, **button_style).pack(pady=5)

    # Ver miembros
    def mostrar_lista_miembros():
        equipo.cargar_datos_equipo()
        if not equipo.supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores disponibles.")
            return

        ventana_ver = Toplevel()
        ventana_ver.title("Ver Miembros por Supervisor")
        ventana_ver.geometry("400x350")
        ventana_ver.configure(bg=DARK_BG)

        tk.Label(ventana_ver, text="Seleccioná un supervisor:", font=("Helvetica", 10), bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        var_sup = tk.StringVar()
        combo = ttk.Combobox(ventana_ver, textvariable=var_sup, state="readonly")
        combo["values"] = [s.nombre for s in equipo.supervisores]
        combo.pack()

        text_frame = tk.Frame(ventana_ver, bg=DARK_BG)
        text_frame.pack(padx=10, pady=10, fill="both", expand=True)

        area_texto = tk.Text(text_frame, width=40, height=12, bg=TEXT_BG, fg=DARK_FG)
        area_texto.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(text_frame, command=area_texto.yview)
        scrollbar.pack(side="right", fill="y")
        area_texto.config(yscrollcommand=scrollbar.set)
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

        tk.Button(ventana_ver, text="Mostrar miembros", command=mostrar, **button_style).pack()

    tk.Button(frame, text="Ver miembros", width=30, command=mostrar_lista_miembros, **button_style).pack(pady=5)

    # Eliminar miembro
    def mostrar_formulario_eliminar_miembro():
        equipo.cargar_datos_equipo()
        if not equipo.supervisores:
            messagebox.showinfo("Sin supervisores", "No hay supervisores disponibles.")
            return

        ventana_eliminar = Toplevel()
        ventana_eliminar.title("Eliminar Miembro")
        ventana_eliminar.geometry("350x300")
        ventana_eliminar.configure(bg=DARK_BG)

        tk.Label(ventana_eliminar, text="Supervisor:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        supervisor_var = tk.StringVar()
        supervisor_combo = ttk.Combobox(ventana_eliminar, textvariable=supervisor_var, state="readonly")
        supervisor_combo["values"] = [s.nombre for s in equipo.supervisores]
        supervisor_combo.pack()

        tk.Label(ventana_eliminar, text="Miembro:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        miembro_var = tk.StringVar()
        miembro_combo = ttk.Combobox(ventana_eliminar, textvariable=miembro_var, state="readonly")
        miembro_combo.pack()

        mensaje = tk.Label(ventana_eliminar, text="", fg="green", bg=DARK_BG)
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
                messagebox.showinfo("Miembro eliminado", "Las tareas asignadas a este miembro se han desasignado.")
                supervisor_combo.set("")
                for t in tareas.tareas:
                    if t.get("miembro") == nombre_miembro:
                        t["asignada"] = False
                        t["miembro"] = None
                tareas.guardar_datos_tareas()
                sincronizar_tareas_en_equipo()
                equipo.cargar_datos_equipo()
                actualizar_miembros(None)
            else:
                mensaje.config(text="No se pudo eliminar.", fg="red")

        tk.Button(ventana_eliminar, text="Eliminar", command=procesar_eliminacion, **button_style).pack(pady=10)

    tk.Button(frame, text="Eliminar miembro", width=30, command=mostrar_formulario_eliminar_miembro, **button_style).pack(pady=5)
    
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
        ventana_mod.geometry("350x300")
        ventana_mod.configure(bg=DARK_BG)

        tk.Label(ventana_mod, text="Supervisor:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        var_sup = tk.StringVar()
        combo_sup = ttk.Combobox(ventana_mod, textvariable=var_sup, state="readonly")
        combo_sup["values"] = [s.nombre for s in equipo.supervisores]
        combo_sup.pack()

        tk.Label(ventana_mod, text="Miembro:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        var_miembro = tk.StringVar()
        combo_miembro = ttk.Combobox(ventana_mod, textvariable=var_miembro, state="readonly")
        combo_miembro.pack()

        tk.Label(ventana_mod, text="Nuevo rol:", bg=DARK_BG, fg=DARK_FG).pack(pady=2)
        var_rol = tk.StringVar()
        combo_rol = ttk.Combobox(ventana_mod, textvariable=var_rol, state="readonly")
        combo_rol["values"] = roles.roles
        combo_rol.pack()

        mensaje = tk.Label(ventana_mod, text="", fg="green", bg=DARK_BG)
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

        tk.Button(ventana_mod, text="Modificar", command=modificar, **button_style).pack(pady=10)

    tk.Button(frame, text="Modificar miembro", width=30, command=mostrar_formulario_modificar_miembro, **button_style).pack(pady=5)

    tk.Button(frame, text="Volver al menú Equipo", width=30, command=lambda: mostrar_frame("equipo"), **button_style).pack(pady=15)

# ==== MENÚ ROLES ====
def crear_menu_roles():
    frame = tk.Frame(contenedor, bg=DARK_BG)
    frames["roles"] = frame

    tk.Label(frame, text="Menú Roles", font=(FONT_FAMILY, current_font_size+2, "bold"), 
             bg=DARK_BG, fg=ACCENT_COLOR).pack(pady=10)

    button_style = {'bg': BUTTON_BG, 'fg': DARK_FG, 'font': (FONT_FAMILY, current_font_size), 
                    'activebackground': HOVER_COLOR, 'activeforeground': 'white', 
                    'relief': 'flat', 'borderwidth': 0, 'padx': 10, 'pady': 5}

    #Agregar rol
    def mostrar_formulario_agregar_rol():
        roles.cargar_datos_roles()

        ventana = Toplevel()
        ventana.title("Agregar Rol")
        ventana.geometry("350x200")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Nombre del nuevo rol:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        entrada = tk.Entry(ventana, bg=ENTRY_BG, fg=DARK_FG, insertbackground=DARK_FG)
        entrada.pack()

        mensaje = tk.Label(ventana, text="", fg="green", bg=DARK_BG)
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

        tk.Button(ventana, text="Agregar", command=agregar, **button_style).pack(pady=10)

    tk.Button(frame, text="Agregar nuevo rol", width=30, command=mostrar_formulario_agregar_rol, **button_style).pack(pady=5)
    
    # Ver roles disponibles
    def mostrar_lista_roles():
        roles.cargar_datos_roles()
        if not roles.roles:
            messagebox.showinfo("Sin roles", "No hay roles registrados.")
            return

        ventana = Toplevel()
        ventana.title("Roles disponibles")
        ventana.geometry("350x300")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Lista de roles:", font=("Helvetica", 12), bg=DARK_BG, fg=DARK_FG).pack(pady=8)

        text_frame = tk.Frame(ventana, bg=DARK_BG)
        text_frame.pack(padx=10, pady=5, fill="both", expand=True)

        area = tk.Text(text_frame, width=30, height=12, bg=TEXT_BG, fg=DARK_FG)
        area.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(text_frame, command=area.yview)
        scrollbar.pack(side="right", fill="y")
        area.config(yscrollcommand=scrollbar.set)

        for rol in roles.roles:
            area.insert(tk.END, f"- {rol}\n")
        area.config(state=tk.DISABLED)

    tk.Button(frame, text="Ver roles disponibles", width=30, command=mostrar_lista_roles, **button_style).pack(pady=5)

    # Eliminar rol
    def mostrar_formulario_eliminar_rol():
        roles.cargar_datos_roles()
        if not roles.roles:
            messagebox.showinfo("Sin roles", "No hay roles para eliminar.")
            return

        ventana = Toplevel()
        ventana.title("Eliminar Rol")
        ventana.geometry("350x250")
        ventana.configure(bg=DARK_BG)

        tk.Label(ventana, text="Seleccioná un rol:", bg=DARK_BG, fg=DARK_FG).pack(pady=5)
        seleccion = tk.StringVar()
        combo = ttk.Combobox(ventana, textvariable=seleccion, state="readonly")
        combo["values"] = roles.roles
        combo.pack(pady=5)

        mensaje = tk.Label(ventana, text="", fg="red", bg=DARK_BG)
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

        tk.Button(ventana, text="Eliminar", command=eliminar, **button_style).pack(pady=10)

    tk.Button(frame, text="Eliminar rol", width=30, command=mostrar_formulario_eliminar_rol, **button_style).pack(pady=5)

    tk.Button(frame, text="Volver al Menú Equipo", width=30, command=lambda: mostrar_frame("equipo"), **button_style).pack(pady=5)
    tk.Button(frame, text="Volver al Menú Principal", width=30, command=lambda: mostrar_frame("principal"), **button_style).pack(pady=5)

def sincronizar_tareas_en_equipo():
    equipo.cargar_datos_equipo()
    tareas.cargar_datos_tareas()

    for sup in equipo.supervisores:
        for persona in sup.equipo.miembros:
            persona.tareas.clear()

    for t in tareas.tareas:
        if t.get("asignada"):
            for sup in equipo.supervisores:
                for persona in sup.equipo.miembros:
                    if persona.nombre == t["miembro"]:
                        persona.asignar_tarea(t["nombre"])

    equipo.guardar_datos_equipo()

def hay_miembros():
    equipo.cargar_datos_equipo()
    return any(s.equipo.miembros for s in equipo.supervisores)

def hay_tareas():
    tareas.cargar_datos_tareas()
    return len(tareas.tareas) > 0

def hay_tareas_asignadas():
    tareas.cargar_datos_tareas()
    return any(t.get("asignada") for t in tareas.tareas)

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
    crear_menu_ver_tareas()

    mostrar_frame("principal")
    ventana.mainloop()