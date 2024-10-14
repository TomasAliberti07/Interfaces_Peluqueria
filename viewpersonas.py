import tkinter as tk
from tkinter import ttk
import mysql.connector

class ViewPersonas(tk.Frame):
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
        search_frame = tk.LabelFrame(self, text="Buscar por DNI", bg="#40E0D0", font=('Calibri', 20), borderwidth=5)
        search_frame.grid(row=0, column=0, padx=5, pady=20, sticky="ew")

        # Entrada de búsqueda
        self.search_entry = tk.Entry(search_frame, width=20, font=('Calibri', 15))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botón de búsqueda
        search_button = tk.Button(search_frame, text="Buscar", command=self.search_personas, bg="#ffffff", font=('Calibri', 15))
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Treeview de personas
        self.personas_treeview = ttk.Treeview(self, columns=("dni", "nombre", "apellido", "telefono", "correo", "domicilio", "ciudad", "instagram"), show="headings")
        self.personas_treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Configuración del Treeview
        self.personas_treeview.heading("nombre", text="Nombre")
        self.personas_treeview.heading("apellido", text="Apellido")
        self.personas_treeview.heading("dni", text="DNI")
        self.personas_treeview.heading("correo", text="Correo")
        self.personas_treeview.heading("telefono", text="Teléfono")


        # Ancho de las columnas y datos centrados
        self.personas_treeview.column("nombre", anchor='center', width=150)
        self.personas_treeview.column("apellido", anchor='center', width=150)
        self.personas_treeview.column("dni", anchor='center', width=150)
        self.personas_treeview.column("correo", anchor='center', width=150)
        self.personas_treeview.column("telefono", anchor='center', width=150)

        # Carga los datos iniciales
        self.load_personas()

    def load_personas(self):
        self.mycursor.execute("SELECT * FROM persona ")#filtrar solo activos.
        personas = self.mycursor.fetchall()
        for persona in personas:
            self.personas_treeview.insert("", "end", values=(persona[1], persona[2], persona[3], persona[4], persona[5], persona[6], persona[7], persona[8]))

    def search_personas(self):
        dni = self.search_entry.get()
        if dni:
            self.mycursor.execute("SELECT * FROM persona WHERE dni = %s", (dni,))
            personas = self.mycursor.fetchall()
            self.personas_treeview.delete(*self.personas_treeview.get_children())
            for persona in personas:
                self.personas_treeview.insert("", "end", values=(persona[1], persona[2], persona[3], persona[4], persona[5], persona[6], persona[7], persona[8]))

    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
    app = ViewPersonas(root)
    app.mainloop()