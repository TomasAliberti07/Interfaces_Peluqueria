import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import mysql.connector
from tkinter import messagebox

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="base_peluqueria"
)
cursor = db.cursor()

# Función para registrar turno en la base de datos
def mostrar_turnos():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT fecha, hora, nombre_cliente, nombre FROM turno JOIN servicio ON turno.id_servicio = servicio.id_servicio")
    turnos = cursor.fetchall()
    
    for turno in turnos:
        tree.insert("", "end", values=turno)

def registrar_turno():
    fecha = cal.get_date()
    hora = entry_hora.get()
    nombre_cliente = entry_cliente.get()
    servicio = combo_servicio.get()

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

# Ventana principal
root = tk.Tk()
root.title("Gestor de Turnos")
root.geometry("800x400")

# Sección izquierda: Ingreso de datos
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

label_fecha = tk.Label(frame_left, text="Fecha:")
label_fecha.pack()
cal = Calendar(frame_left, date_pattern='y-mm-dd')
cal.pack(pady=5)

label_hora = tk.Label(frame_left, text="Hora (HH:MM):")
label_hora.pack()
entry_hora = tk.Entry(frame_left)
entry_hora.pack(pady=5)

label_cliente = tk.Label(frame_left, text="Nombre del Cliente:")
label_cliente.pack()
entry_cliente = tk.Entry(frame_left)
entry_cliente.pack(pady=5)

label_servicio = tk.Label(frame_left, text="Servicio:")
label_servicio.pack()
combo_servicio = ttk.Combobox(frame_left)
combo_servicio.pack(pady=5)

# Obtener los servicios disponibles de la base de datos
cursor.execute("SELECT nombre FROM servicio")
servicios = cursor.fetchall()
combo_servicio['values'] = [servicio[0] for servicio in servicios]

button_registrar = tk.Button(frame_left, text="Registrar Turno", command=registrar_turno)
button_registrar.pack(pady=20)

# Sección derecha: Grilla de turnos
frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

columns = ("Fecha", "Hora", "Nombre Cliente", "Servicio")
tree = ttk.Treeview(frame_right, columns=columns, show='headings')
tree.heading("Fecha", text="Fecha")
tree.heading("Hora", text="Hora")
tree.heading("Nombre Cliente", text="Nombre Cliente")
tree.heading("Servicio", text="Servicio")
tree.pack()

# Mostrar los turnos al iniciar
mostrar_turnos()

root.mainloop()
