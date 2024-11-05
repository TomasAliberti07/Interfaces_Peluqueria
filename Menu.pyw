import tkinter as tk
from tkinter import PhotoImage, Toplevel
from viewpersonas import ViewPersonas  # Importamos la clase ViewPersonas
from viewserviciosSEGUNDO import VerServicios
from alta_turnos import iniciar_turnero
from view_productos import ListadoProductos

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)  # Hacer que la ventana sea de pantalla completa
        self.resizable(False, False)  # Deshabilitar el redimensionamiento
        self.configure(bg="#40E0D0")
        self.title("Menu")

        # Cargar imagen
        ruta_imagen = 'C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen4.png'
        self.imagen = PhotoImage(file=ruta_imagen)

        # Crear un frame principal para centrar el contenido
        main_frame = tk.Frame(self, bg=self.cget('bg'))
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrar el frame en la ventana

        # Etiqueta para mostrar la imagen
        self.label_imagen = tk.Label(main_frame, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=0, column=0, columnspan=5, padx=1, pady=10)

        # Crear un frame para los botones
        button_frame = tk.Frame(main_frame, bg=self.cget('bg'))
        button_frame.grid(row=1, column=0, columnspan=5, padx=20, pady=10)

        # Configurar el grid para centrar los botones en el button_frame
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)

        # Botones con fuente más grande
        tk.Button(button_frame, text="Turnos", font=("Calibri", 20), width=10, command=self.abrir_gestion_turnos).grid(row=0, column=0, padx=30, pady=10)
        tk.Button(button_frame, text="Personas", font=("Calibri", 20), width=10, command=self.personas).grid(row=0, column=1, padx=30, pady=10)
        tk.Button(button_frame, text="Stock", font=("Calibri", 20), width=10, command=self.stock).grid(row=0, column=2, padx=30, pady=10)
        tk.Button(button_frame, text="Servicios", font=("Calibri", 20), width=10, command=self.servicios).grid(row=0, column=3, padx=30, pady=10)

        # Botón de Cerrar
        tk.Button(button_frame, text="Cerrar", font=("Calibri", 20), width=10, command=self.cerrar).grid(row=0, column=4, padx=30, pady=10)

    def cerrar(self):
        self.destroy()  # Cierra la aplicación

    def abrir_gestion_turnos(self):
        # Oculta la ventana del menú antes de abrir la ventana de turnos
        self.withdraw()  # Oculta la ventana del menú
        iniciar_turnero(self)  # Pasa la ventana del menú como argument

    def personas(self):
        self.withdraw()  # Oculta la ventana del menú
        ventana_personas = Toplevel(self)
        ventana_personas.title("Visualizar Personas")
        ventana_personas.resizable(False, False)
        ViewPersonas(ventana_personas)

    def stock(self):
        self.withdraw()
        ListadoProductos(self)

    def servicios(self):
        ventana_servicios = Toplevel(self)
        ventana_servicios.title("Servicios")
        ventana_servicios.geometry("800x550")
        ventana_servicios.title("Visualizar Personas") 
        ventana_servicios.resizable(False, False)  # Deshabilitar el redimensionamiento
        VerServicios(ventana_servicios) 

if __name__ == "__main__":
    menu = Menu()
    menu.mainloop()
