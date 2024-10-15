import tkinter as tk
from tkinter import ttk
import mysql.connector

class ViewServicios(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#40E0D0", width=1366, height=768)
        self.master = master
        self.grid_propagate(False)  # Evita que el frame cambie de tamaño
        self.grid(row=0, column=0, sticky="nsew")

        # Conectar a la base de datos y crear un cursor
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto por tu usuario
            password="123",  # Cambia esto por tu contraseña
            database="base_peluqueria"  # Cambia esto por tu base de datos
        )
        self.mycursor = self.mydb.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Frame de búsqueda
        search_frame = tk.LabelFrame(self, text="Buscar por Servicio", bg="#40E0D0", font=('Calibri', 20), borderwidth=5)
        search_frame.grid(row=0, column=0, padx=5, pady=20, sticky="ew")

        # Entrada de búsqueda
        self.search_entry = tk.Entry(search_frame, width=20, font=('Calibri', 15))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botón de búsqueda
        search_button = tk.Button(search_frame, text="Buscar Servicio", command=self.search_servicios, bg="#ffffff", font=('Calibri', 15))
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Treeview de servicios
        self.servicios_treeview = ttk.Treeview(self, columns=("Nombre", "Descripcion", "Tiempo Estimado"), show="headings")
        self.servicios_treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Configuración del Treeview
        self.servicios_treeview.heading("nombre", text="Nombre")
        self.servicios_treeview.heading("descripcion", text="Descripcion")
        self.servicios_treeview.heading("tiempo", text="Tiempo Estimado")


        # Ancho de las columnas y datos centrados
        self.servicios_treeview.column("nombre", anchor='center', width=150)
        self.servicios_treeview.column("descripcion", anchor='center', width=150)
        self.servicios_treeview.column("tiempo", anchor='center', width=150)

        # Carga los datos iniciales
        self.load_servicios()

    def load_servicios(self):
        self.mycursor.execute("SELECT * FROM servicio")#filtrar solo activos.
        servicios = self.mycursor.fetchall()
        for servicio in servicios:
            self.servicios_treeview.insert("", "end", values=(servicio[1], servicio[2], servicio[3], servicio[4], servicio[5], servicio[6], servicio[7], servicio[8]))

    def search_servicios(self):
        dni = self.search_entry.get()
        if dni:
            self.mycursor.execute("SELECT * FROM servicio WHERE nombre = %s", (dni,))
            servicios = self.mycursor.fetchall()
            self.servicios_treeview.delete(*self.servicios_treeview.get_children())
            for servicio in servicios:
                self.servicios_treeview.insert("", "end", values=(servicio[1], servicio[2], servicio[3], servicio[4], servicio[5], servicio[6], servicio[7], servicio[8]))

    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
    app = Viewservicios(root)
    app.mainloop()
