import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import mysql.connector
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk

def iniciar_turnero(menu_ventana):
    # Conexión a la base de datos
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="base_peluqueria"
    )
    cursor = db.cursor()

    def mostrar_turnos(fecha=None):
        for row in tree.get_children():
            tree.delete(row)
        if cursor.stored_results():
            cursor.fetchall()
        if fecha:
            cursor.execute("SELECT fecha, hora, nombre_cliente, nombre FROM turno JOIN servicio ON turno.id_servicio = servicio.id_servicio WHERE fecha = %s ORDER BY fecha DESC", (fecha,))
        else:
            cursor.execute("SELECT fecha, hora, nombre_cliente, nombre FROM turno JOIN servicio ON turno.id_servicio = servicio.id_servicio ORDER BY fecha DESC")
        turnos = cursor.fetchall()
        for turno in turnos:
            tree.insert("", "end", values=turno)

    def filtrar_por_fecha():
        fecha_seleccionada = cal.get_date()
        mostrar_turnos(fecha_seleccionada)

    def registrar_turno():
        fecha = cal.get_date()
        hora = entry_hora.get()
        nombre_cliente = entry_cliente.get()
        servicio = combo_servicio.get()
        if not fecha or not hora or not nombre_cliente or not servicio:
            messagebox.showerror("Error", "Todos los campos deben estar completos.")
            return
        nombre_cliente = nombre_cliente.upper()
        servicio = servicio.upper()
        fecha_actual = datetime.now().date()
        fecha_turno = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_turno < fecha_actual:
            messagebox.showerror("Error", "No se pueden registrar turnos en fechas anteriores a hoy.")
            return
        cursor.execute("SELECT id_servicio FROM servicio WHERE UPPER(nombre) = %s", (servicio,))
        id_servicio = cursor.fetchone()
        if id_servicio:
            cursor.execute("INSERT INTO turno (fecha, hora, id_servicio, nombre_cliente) VALUES (%s, %s, %s, %s)", (fecha, hora, id_servicio[0], nombre_cliente))
            db.commit()
            messagebox.showinfo("Éxito", "Turno registrado correctamente")
            mostrar_turnos()
        else:
            messagebox.showerror("Error", "Servicio no encontrado")

    def cargar_turno_seleccionado(event):
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, 'values')
            entry_hora.delete(0, tk.END)
            entry_hora.insert(0, item_values[1])
            entry_cliente.delete(0, tk.END)
            entry_cliente.insert(0, item_values[2])
            combo_servicio.set(item_values[3])
            global turno_id
            if cursor.stored_results():
                cursor.fetchall()
            cursor.execute("SELECT id_turno FROM turno WHERE fecha = %s AND hora = %s AND nombre_cliente = %s", (item_values[0], item_values[1], item_values[2]))
            turno_id = cursor.fetchone()[0]

    def modificar_turno():
        global turno_id
        if not turno_id:
            messagebox.showerror("Error", "No se ha seleccionado ningún turno para modificar.")
            return
        fecha = cal.get_date()
        hora = entry_hora.get().upper()
        nombre_cliente = entry_cliente.get().upper()
        servicio = combo_servicio.get().upper()
        cursor.execute("SELECT id_servicio FROM servicio WHERE UPPER(nombre) = %s", (servicio,))
        id_servicio = cursor.fetchone()
        if id_servicio:
            cursor.execute("UPDATE turno SET fecha = %s, hora = %s, id_servicio = %s, nombre_cliente = %s WHERE id_turno = %s", (fecha, hora, id_servicio[0], nombre_cliente, turno_id))
            db.commit()
            messagebox.showinfo("Éxito", "Turno modificado correctamente")
            mostrar_turnos()
        else:
            messagebox.showerror("Error", "Servicio no encontrado")

    def eliminar_turno():
        global turno_id
        if not turno_id:
            messagebox.showerror("Error", "No se ha seleccionado ningún turno para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este turno?")
        if confirm:
            cursor.execute("DELETE FROM turno WHERE id_turno = %s", (turno_id,))
            db.commit()
            messagebox.showinfo("Éxito", "Turno eliminado correctamente")
            mostrar_turnos()
            turno_id = None

# Configuración de la ventana principal
    root = tk.Toplevel(menu_ventana)
    root.attributes("-fullscreen", True)  # Establece la ventana en pantalla completa
    root.title("Sistema de Turnos de Peluquería")
    root.configure(background='#008B8B')

    # Diseño ajustable
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.rowconfigure(0, weight=1)

        # Frame izquierdo
    frame_left = tk.Frame(root, bg='#66CCCC')
    frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Ajusta el calendario en un Frame para que ocupe el 60% del espacio vertical
    frame_cal = tk.Frame(frame_left, bg='#66CCCC', height=int(root.winfo_screenheight() * 0.6))
    frame_cal.pack(pady=5, fill="both", expand=True)

    label_fecha = tk.Label(frame_cal, text="Fecha:", bg='#66CCCC', font=("Arial", 14))
    label_fecha.pack()

    cal = Calendar(frame_cal, date_pattern='y-mm-dd', background='#66CCCC', foreground='black', borderwidth=1)
    cal.pack(pady=5, fill="x")  # Ajusta el tamaño en función del contenedor

        # Cargar y mostrar el logo en la ubicación marcada
    # Cargar y mostrar el logo en la ubicación marcada
    try:
        logo_path = "C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen4.png"  # Ruta de la imagen del logo
        logo = Image.open(logo_path)
        logo = logo.resize((250, 150), Image.LANCZOS)  # Ajustar el tamaño del logo
        logo_tk = ImageTk.PhotoImage(logo)

        # Frame intermedio para centrar el logo
        frame_logo = tk.Frame(frame_cal, bg='#66CCCC', height=-250)  # Ajusta la altura según lo necesites
        frame_logo.pack(pady=5)  # Ajusta el espacio superior e inferior según sea necesario

        label_logo = tk.Label(frame_logo, image=logo_tk, bg='#66CCCC')
        label_logo.image = logo_tk  # Mantener una referencia para evitar que se elimine
        label_logo.pack()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")
     # Botón de mostrar todos los turnos
    button_mostrar_todos = tk.Button(frame_left, text="Mostrar Todos los Turnos", command=mostrar_turnos, bg='#F7F7F7', font=("Arial", 12))
    button_mostrar_todos.pack(pady=10, fill="x")  # Ajuste el espacio y tamaño del botón
    # Ajusta el botón de filtro y demás elementos más cerca del calendario y con un tamaño mayor
    button_filtrar = tk.Button(frame_left, text="Filtrar Turnos por Fecha", command=filtrar_por_fecha, bg='#F7F7F7', font=("Arial", 12))
    button_filtrar.pack(pady=(5, 5), fill="x")  # Reduce el padding superior

    label_hora = tk.Label(frame_left, text="Hora (HH:MM):", bg='#66CCCC', font=("Arial", 12))
    label_hora.pack(pady=(5, 2))  # Espaciado reducido
    entry_hora = tk.Entry(frame_left, font=("Arial", 12))
    entry_hora.insert(0, "HH:MM")
    entry_hora.pack(pady=2, fill="x")  # Ajuste para reducir el espacio

    label_cliente = tk.Label(frame_left, text="Nombre del Cliente:", bg='#66CCCC', font=("Arial", 12))
    label_cliente.pack(pady=(5, 2))
    entry_cliente = tk.Entry(frame_left, font=("Arial", 12))
    entry_cliente.pack(pady=2, fill="x")

    label_servicio = tk.Label(frame_left, text="Servicio:", bg='#66CCCC', font=("Arial", 12))
    label_servicio.pack(pady=(5, 2))
    combo_servicio = ttk.Combobox(frame_left, font=("Arial", 12))
    combo_servicio.pack(pady=2, fill="x")

    cursor.execute("SELECT nombre FROM servicio")
    servicios = cursor.fetchall()
    combo_servicio['values'] = [servicio[0] for servicio in servicios]

    # Frame derecho (se mantiene igual)
    frame_right = tk.Frame(root, bg='#66CCCC')
    frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    label_turnos = tk.Label(frame_right, text="Turnos Registrados", font=("Arial", 20), bg='#66CCCC')
    label_turnos.pack(pady=5)

    columns = ("Fecha", "Hora", "Nombre Cliente", "Servicio")
    tree = ttk.Treeview(frame_right, columns=columns, show='headings', selectmode='browse')
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")
    tree.heading("Nombre Cliente", text="Nombre Cliente")
    tree.heading("Servicio", text="Servicio")
    tree.pack(pady=10, fill="both", expand=True)

    tree.bind("<<TreeviewSelect>>", cargar_turno_seleccionado)

    # Frame de botones
    frame_botones = tk.Frame(frame_right, bg='#66CCCC')
    frame_botones.pack(pady=20)

    button_registrar = tk.Button(frame_botones, text="Registrar Turno", command=registrar_turno, bg='#F7F7F7', font=("Arial", 12))
    button_registrar.pack(side=tk.LEFT, padx=10)

    button_modificar = tk.Button(frame_botones, text="Modificar Turno", command=modificar_turno, bg='#F7F7F7', font=("Arial", 12))
    button_modificar.pack(side=tk.LEFT, padx=10)

    button_eliminar = tk.Button(frame_botones, text="Eliminar Turno", command=eliminar_turno, bg='#F7F7F7', font=("Arial", 12))
    button_eliminar.pack(side=tk.LEFT, padx=10)

    button_volver = tk.Button(frame_botones, text="Volver", command=root.destroy, bg='#F7F7F7', font=("Arial", 12))
    button_volver.pack(side=tk.LEFT, padx=10)

    mostrar_turnos()

    turno_id = None
    root.mainloop()