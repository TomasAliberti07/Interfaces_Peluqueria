import tkinter as tk
from tkinter import ttk,PhotoImage, messagebox
import mysql.connector


class ViewPersonas(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#008B8B", width=1366, height=768)
        self.master = master
        self.grid_propagate(False)  # Evita que el frame cambie de tamaño
        self.grid(row=0, column=0, sticky="nsew")
        ruta_imagen = 'C:/Users/GUILLERMINA/Desktop/Interfaces_Peluqueria/imagen3.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        
        self.label_imagen = tk.Label(self, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=4, column=0, rowspan=3, padx=20, pady=10)

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
        search_button = tk.Button(search_frame, text="Modificiar", command=self.eliminar_persona, bg="#ffffff", font=('Calibri', 15),width=8)
        search_button.grid(row=0, column=3, padx=10, pady=10)
        search_button = tk.Button(search_frame, text="Eliminar", command=self.eliminar_persona, bg="#ffffff", font=('Calibri', 15),width=8)
        search_button.grid(row=0, column=4, padx=10, pady=10)
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
        self.mycursor.execute("SELECT * FROM persona WHERE activo = 'si'")  # Filtrar solo activos
        personas = self.mycursor.fetchall()
       #IMPORTANTE CORREGIR CADA UNO SEGUN LA BASE DE DATOS QUE TENGA LA POSION DE CADA ATRIBUTO EJ:EN MI BASE DE DATOS TENGO DNI EN LA POSION 3 POR ESO PERSONA[3]
        for persona in personas:
            self.personas_treeview.insert("", "end", values=(persona[3], persona[1], persona[2], persona[4], persona[9], persona[5], persona[6], persona[7], persona[8]))

    def search_personas(self):
        dni = self.search_entry.get()
        if dni:
            self.mycursor.execute("SELECT * FROM persona WHERE dni = %s", (dni,))  
            personas = self.mycursor.fetchall()
            self.personas_treeview.delete(*self.personas_treeview.get_children())
            #Repetir procedimiento en la linea 87
            for persona in personas:
                self.personas_treeview.insert("", "end", values=(persona[3], persona[1], persona[2], persona[4], persona[9], persona[5], persona[6], persona[7], persona[8]))

    def eliminar_persona(self):
        selected_item = self.personas_treeview.selection()  # Obtiene el ítem seleccionado
        if not selected_item:  # Verifica si no hay selección
          messagebox.showwarning("Advertencia", "Por favor, selecciona una persona para eliminar.")  # Línea añadida
          return  # Salir si no hay selección
        if selected_item:
            persona_dni = self.personas_treeview.item(selected_item, 'values')[0]  
            confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar a la persona con DNI {persona_dni}?")
            if confirm:
                self.mycursor.execute("UPDATE persona SET activo = 'no' WHERE dni = %s", (persona_dni,))
                self.mydb.commit()  #
                self.load_personas() 
    
            

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
       self.master.destroy()  # Cierra la ventana actual
       from Menu import Menu  # Importa la clase Menu
       menu = Menu(self.master)  # Crea una instancia de Menu
       menu.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
    app = ViewPersonas(root)
    app.mainloop()
