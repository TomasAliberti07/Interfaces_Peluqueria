import tkinter as tk
from tkinter import ttk,PhotoImage
import mysql.connector


class ViewPersonas(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#008B8B", width=1366, height=768)
        self.master = master
        self.grid_propagate(False)  # Evita que el frame cambie de tamaño
        self.grid(row=0, column=0, sticky="nsew")
        ruta_imagen = 'C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen4.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        
        self.label_imagen = tk.Label(self, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=4, column=0, rowspan=3, padx=20, pady=10)

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
        search_frame = tk.LabelFrame(self, text="Buscar por DNI", bg="#008B8B", font=('Calibri', 20), borderwidth=5)
        search_frame.grid(row=0, column=0, padx=70, pady=20, sticky="ew")

        # Entrada de búsqueda
        self.search_entry = tk.Entry(search_frame, width=20, font=('Calibri', 15))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botón de búsqueda
        search_button = tk.Button(search_frame, text="Buscar", command=self.search_personas, bg="#ffffff", font=('Calibri', 15),width=8)
        search_button.grid(row=0, column=1, padx=10, pady=10)
        search_button = tk.Button(search_frame, text="+Agregar", command=self.abrir_altap, bg="#ffffff", font=('Calibri', 15),width=8)
        search_button.grid(row=0, column=2, padx=10, pady=10)
        back_button = tk.Button(self, text="Volver", command=self.volver_menu, bg="#ffffff", font=('Calibri', 15),width=8)
        back_button.grid(row=2, column=0, padx=10, pady=10)
        style = ttk.Style()
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#ffffff")
        
        # Treeview de personas
        self.personas_treeview = ttk.Treeview(self, columns=("dni", "nombre", "apellido", "contacto", "correo", "tipo", "activo", "id_tipo_p", "id_turno"), show="headings")
        self.personas_treeview.grid(row=1, column=0, sticky="nsew", padx=70, pady=10)

        # Configuración del Treeview
        self.personas_treeview.heading("nombre", text="Nombre")
        self.personas_treeview.heading("apellido", text="Apellido")
        self.personas_treeview.heading("dni", text="DNI")
        self.personas_treeview.heading("contacto", text="Contacto")
        self.personas_treeview.heading("correo", text="Correo")
        self.personas_treeview.heading("tipo", text="Tipo")
        self.personas_treeview.heading("activo", text="Activo")
        self.personas_treeview.heading("id_tipo_p", text="Tipo ID")
        self.personas_treeview.heading("id_turno", text="Turno ID")

        # Ancho de las columnas y datos centrados
        self.personas_treeview.column("nombre", anchor='center', width=150)
        self.personas_treeview.column("apellido", anchor='center', width=150)
        self.personas_treeview.column("dni", anchor='center', width=150)
        self.personas_treeview.column("contacto", anchor='center', width=150)
        self.personas_treeview.column("correo", anchor='center', width=150)
        self.personas_treeview.column("tipo", anchor='center', width=150)
        self.personas_treeview.column("activo", anchor='center', width=100)
        self.personas_treeview.column("id_tipo_p", anchor='center', width=100)
        self.personas_treeview.column("id_turno", anchor='center', width=100)

        # Carga los datos iniciales
        self.load_personas()

    def load_personas(self):
        self.mycursor.execute("SELECT * FROM persona")
        personas = self.mycursor.fetchall()
        for persona in personas:
            # Imprime la tupla persona para ver su estructura
            print(persona)
            # Accede a los índices de manera segura utilizando un bucle for
            values = []
            for i, valor in enumerate(persona):
                values.append(valor)
            self.personas_treeview.insert("", "end", values=values)
    def search_personas(self):
        dni = self.search_entry.get()
        if dni:
            self.mycursor.execute("SELECT * FROM persona WHERE dni = %s", (dni,))
            personas = self.mycursor.fetchall()
            self.personas_treeview.delete(*self.personas_treeview.get_children())
            for persona in personas:
                values = []
                for valor in persona:
                    values.append(valor)
                self.personas_treeview.insert("", "end", values=values)
    
    def __del__(self):
        self.mycursor.close()
        self.mydb.close()
        
    def abrir_altap(self):
        #Se llama al modulo dentro de la funcion para evitar problema de importación circular
        from alta_persona2 import AltaPersona
        alta = AltaPersona(self)  # Crea una nueva ventana de alta persona
        alta.transient(self)  # Hacer que sea una ventana secundaria
        alta.grab_set()
    def volver_menu(self):
        
        self.mycursor.close()
        self.mydb.close()
        self.master.destroy()  # Cierra la ventana actual
        from Menu import Menu  # Importa la clase Menu
        menu = Menu()  # Crea una instancia de Menu
        menu.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
    app = ViewPersonas(root)
    app.mainloop()
