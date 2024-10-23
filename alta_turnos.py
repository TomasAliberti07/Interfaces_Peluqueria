import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import mysql.connector
from tkinter import messagebox
from datetime import datetime  # Importar datetime
from PIL import Image, ImageTk  # Importar PIL para manejar imágenes

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="base_peluqueria"
)
cursor = db.cursor()

# Función para mostrar turnos filtrados por fecha
def mostrar_turnos(fecha=None):
    # Limpiar el Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Asegurarse de que no haya resultados no leídos
    if cursor.stored_results():
        cursor.fetchall()  # Descartar cualquier resultado no leído

    # Ejecutar la nueva consulta
    if fecha:
        cursor.execute("SELECT fecha, hora, nombre_cliente, nombre FROM turno JOIN servicio ON turno.id_servicio = servicio.id_servicio WHERE fecha = %s ORDER BY fecha DESC", (fecha,))
    else:
        cursor.execute("SELECT fecha, hora, nombre_cliente, nombre FROM turno JOIN servicio ON turno.id_servicio = servicio.id_servicio ORDER BY fecha DESC")
    
    turnos = cursor.fetchall()
    
    for turno in turnos:
        tree.insert("", "end", values=turno)

# Función para filtrar turnos por la fecha seleccionada
def filtrar_por_fecha():
    fecha_seleccionada = cal.get_date()
    mostrar_turnos(fecha_seleccionada)

def registrar_turno():
    fecha = cal.get_date()
    hora = entry_hora.get()
    nombre_cliente = entry_cliente.get()
    servicio = combo_servicio.get()

    # Validar que la fecha no sea anterior a hoy
    fecha_actual = datetime.now().date()
    fecha_turno = datetime.strptime(fecha, "%Y-%m-%d").date()

    if fecha_turno < fecha_actual:
        messagebox.showerror("Error", "No se pueden registrar turnos en fechas anteriores a hoy.")
        return

    # Obtener el id del servicio seleccionado
    cursor.execute("SELECT id_servicio FROM servicio WHERE nombre = %s", (servicio,))
    id_servicio = cursor.fetchone()

    if id_servicio:
        cursor.execute(
            "INSERT INTO turno (fecha, hora, id_servicio, nombre_cliente) VALUES (%s, %s, %s, %s)",
            (fecha, hora, id_servicio[0], nombre_cliente)
        )
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
        entry_hora.insert(0, item_values[1])  # Hora
        entry_cliente.delete(0, tk.END)
        entry_cliente.insert(0, item_values[2])  # Nombre del Cliente
        combo_servicio.set(item_values[3])  # Servicio
        global turno_id

        # Asegurarse de que no haya resultados no leídos
        if cursor.stored_results():
            cursor.fetchall()  # Descartar cualquier resultado no leído

        # Obtener el id del turno seleccionado
        cursor.execute("SELECT id_turno FROM turno WHERE fecha = %s AND hora = %s AND nombre_cliente = %s", (item_values[0], item_values[1], item_values[2]))
        turno_id = cursor.fetchone()[0]  # Guardar el ID del turno seleccionado
def modificar_turno():
    if not turno_id:
        messagebox.showerror("Error", "No se ha seleccionado ningún turno para modificar.")
        return

    fecha = cal.get_date()
    hora = entry_hora.get()
    nombre_cliente = entry_cliente.get()
    servicio = combo_servicio.get()

    # Obtener el id del servicio seleccionado
    cursor.execute("SELECT id_servicio FROM servicio WHERE nombre = %s", (servicio,))
    id_servicio = cursor.fetchone()

    if id_servicio:
        cursor.execute(
            "UPDATE turno SET fecha = %s, hora = %s, id_servicio = %s, nombre_cliente = %s WHERE id_turno = %s",
            (fecha, hora, id_servicio[0], nombre_cliente, turno_id)
        )
        db.commit()
        messagebox.showinfo("Éxito", "Turno modificado correctamente")
        mostrar_turnos()
    else:
        messagebox.showerror("Error", "Servicio no encontrado")

def eliminar_turno():
    global turno_id
    if not turno_id:
        messagebox.showerror("Error", " No se ha seleccionado ningún turno para eliminar.")
        return

    # Confirmar la eliminación
    confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este turno?")
    if confirm:
        cursor .execute("DELETE FROM turno WHERE id_turno = %s", (turno_id,))
        db.commit()
        messagebox.showinfo("Éxito", "Turno eliminado correctamente")
        mostrar_turnos()
        turno_id = None
def volver():
    # Aquí puedes implementar la lógica para volver a la vista anterior
    # Por ejemplo, si estás en un formulario, puedes cerrarlo o limpiar los campos
    entry_hora.delete(0, tk.END)
    entry_cliente.delete(0, tk.END)
    combo_servicio.set('')
    mostrar_turnos()  # Volver a mostrar la lista de turnos

# Crear la ventana principal
root = tk.Tk()
root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
root.title("Sistema de Turnos de Peluquería")
root.configure(background='#008B8B')  # Establecer el color de fondo de la ventana principal

# Sección izquierda : Ingreso de datos
frame_left = tk.Frame(root, bg='#66CCCC')  # Establecer el color de fondo del frame izquierdo
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

label_fecha = tk.Label(frame_left, text="Fecha:", bg='#66CCCC')  # Establecer el color de fondo del label
label_fecha.pack()
cal = Calendar(frame_left, date_pattern='y-mm-dd', background='#66CCCC', foreground='black', borderwidth=1)
cal.pack(pady=5)

# Mover el botón de filtrar debajo del calendario
button_filtrar = tk.Button(frame_left, text="Filtrar Turnos por Fecha", command=filtrar_por_fecha, bg='#F7F7F7')  # Establecer el color de fondo del botón
button_filtrar.pack(pady=10)

label_hora = tk.Label(frame_left, text="Hora (HH:MM):", bg='#66CCCC')  # Establecer el color de fondo del label
label_hora.pack()

entry_hora = tk.Entry(frame_left)
entry_hora.insert(0, "HH:MM")  # Establecer el valor inicial
entry_hora.pack(pady=5)

label_cliente = tk.Label(frame_left, text="Nombre del Cliente:", bg='#66CCCC')  # Establecer el color de fondo del label
label_cliente.pack()
entry_cliente = tk.Entry(frame_left)
entry_cliente.pack(pady=5)

label_servicio = tk.Label(frame_left, text="Servicio:", bg='#66CCCC')  # Establecer el color de fondo del label
label_servicio.pack()
combo_servicio = ttk.Combobox(frame_left)
combo_servicio.pack(pady=5)

# Obtener los servicios disponibles de la base de datos
cursor.execute("SELECT nombre FROM servicio")
servicios = cursor.fetchall()
combo_servicio['values'] = [servicio[0] for servicio in servicios]

# Sección derecha: Grilla de turnos
frame_right = tk.Frame(root, bg='#66CCCC')  # Establecer el color de fondo del frame derecho
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

label_turnos = tk.Label(frame_right, text="Turnos Registrados", font=("Arial", 20), bg='#66CCCC')  # Establecer el color de fondo del label y aumentar el tamaño de la fuente
label_turnos.pack(pady=5)

# Configuración de la grilla (Treeview)
columns = ("Fecha", "Hora", "Nombre Cliente", "Servicio")
tree = ttk.Treeview(frame_right, columns=columns, show='headings', selectmode='browse')
tree.heading("Fecha", text="Fecha")
tree.heading("Hora", text="Hora")
tree.heading("Nombre Cliente", text="Nombre Cliente")
tree.heading("Servicio", text="Servicio")
tree.pack(pady=10)

# Asignar evento de selección de fila
tree.bind("<<TreeviewSelect>>", cargar_turno_seleccionado)

# Frame para botones
frame_botones = tk.Frame(frame_right, bg='#66CCCC')  # Establecer el color de fondo del frame de botones
frame_botones.pack(pady=20)

# Botones
button_registrar = tk.Button(frame_botones, text="Registrar Turno", command=registrar_turno, bg='#F7F7F7')  # Establecer el color de fondo del botón
button_registrar.pack(side=tk.LEFT, padx=10)

button_modificar = tk.Button(frame_botones, text="Modificar Turno", command=modificar_turno, bg='#F7F7F7')  # Establecer el color de fondo del botón
button_modificar.pack(side=tk.LEFT, padx=10)

button_eliminar = tk.Button(frame_botones, text="Eliminar Turno", command=eliminar_turno, bg='#F7F7F7')  # Establecer el color de fondo del botón
button_eliminar.pack(side=tk.LEFT, padx=10)
# Botón Volver
button_volver = tk.Button(frame_botones, text="Volver", command=volver, bg='#F7F7F7')  # Establecer el color de fondo del botón
button_volver.pack(side=tk.LEFT, padx=10)

# Logo de la peluquería
image = Image.open("C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen3.png")
photo = ImageTk.PhotoImage(image)
logo_label = tk.Label(frame_right, image=photo, bg='#66CCCC')  # Establecer el color de fondo del label
logo_label.image = photo
logo_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

# Mostrar todos los turnos al iniciar
mostrar_turnos()

turno_id = None

root.mainloop()