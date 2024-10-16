import tkinter as tk
from tkinter import ttk
import mysql.connector

class ViewServicios(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#40E0D0", width=700, height=550)
        self.master = master
        self.grid_propagate(False)  # Evita que el frame cambie de tamaño
        self.grid(row=0, column=0, sticky="nsew")

        # Conectar a la base de datos y crear un cursor
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto por tu usuario
            password="",  # Cambia esto por tu contraseña
            database="base_peluquerias"  # Cambia esto por tu base de datos
        )
        self.mycursor = self.mydb.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Frame de búsqueda
        search_frame = tk.LabelFrame(self, text="Buscar por nombre", bg="#40E0D0", font=('Calibri', 20), borderwidth=5)
        search_frame.grid(row=0, column=0, padx=10, pady=20, sticky="w")

        # Entrada de búsqueda
        self.search_entry = tk.Entry(search_frame, width=20, font=('Calibri', 15))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botón de búsqueda
        search_button = tk.Button(search_frame, text="Buscar", command=self.search_servicios, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Botón de agregar
        add_button = tk.Button(search_frame, text="+Agregar", command=self.abrir_alta, bg="#ffffff", font=('Calibri', 15), width=8)
        add_button.grid(row=0, column=2, padx=10, pady=10)

        # Botón de eliminar
        delete_button = tk.Button(search_frame, text="Eliminar", command=self.delete_servicio, bg="#ffffff", font=('Calibri', 15), width=8)
        delete_button.grid(row=0, column=3, padx=10, pady=10)

        # Botón de modificar
        modify_button = tk.Button(search_frame, text="Modificar", command=self.modify_servicio, bg="#ffffff", font=('Calibri', 15), width=8)
        modify_button.grid(row=0, column=4, padx=10, pady=10)

        # Treeview de servicios
        self.servicios_treeview = ttk.Treeview(self, columns=( "nombre", "descripcion", "Tiempo Estimado"), show="headings")
        self.servicios_treeview.grid(row=1, column=0, sticky="w", padx=130, pady=10)

        # Configuración del Treeview
        self.servicios_treeview.heading("nombre", text="Nombre")
        self.servicios_treeview.heading("descripcion", text="Descripción")
        self.servicios_treeview.heading("Tiempo Estimado", text="Tiempo Estimado")

        # Ancho de las columnas y datos centrados
        self.servicios_treeview.column("nombre", anchor='center', width=150)
        self.servicios_treeview.column("descripcion", anchor='center', width=200)
        self.servicios_treeview.column("Tiempo Estimado", anchor='center', width=100)

        # Carga los servicios
        self.load_servicios()

    def load_servicios(self):
        self.mycursor.execute("SELECT * FROM servicio")
        servicios = self.mycursor.fetchall()
        for servicio in servicios:
            self.servicios_treeview.insert("", "end", values=(servicio[3], servicio[1], servicio[2]))

    def search_servicios(self):
        nombre = self.search_entry.get()
        if nombre:
            self.mycursor.execute("SELECT * FROM servicio WHERE nombre = %s", (nombre,))
            servicios = self.mycursor.fetchall()
            self.servicios_treeview.delete(*self.servicios_treeview.get_children())
            for servicio in servicios:
                self.servicios_treeview.insert("", "end", values=( servicio[3], servicio[1], servicio[2]))

    def delete_servicio(self):
        # Implementar lógica para eliminar un servicio seleccionado
        pass

    def modify_servicio(self):
        # Implementar lógica para modificar un servicio seleccionado
        pass

    def abrir_alta(self):
        # Se llama al módulo dentro de la función para evitar problema de importación circular
        from alta_servicio import AltaServicio
        alta = AltaServicio(self)  # Crea una nueva ventana de alta servicio
        alta.transient(self)  # Hacer que sea una ventana secundaria
        alta.grab_set()

    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Listado de servicios")
    root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
    app = ViewServicios(root)
    app.mainloop()