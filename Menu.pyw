import tkinter as tk
from tkinter import PhotoImage, Toplevel
from viewpersonas import ViewPersonas  # Importamos la clase ViewPersonas
from viewserviciosSEGUNDO import VerServicios
from alta_turnos import iniciar_turnero
from view_productos import ListadoProductos

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#40E0D0")
        self.title("Menu")

        # Cargar imagen
        ruta_imagen = 'C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen4.png'
        self.imagen = PhotoImage(file=ruta_imagen)

        # Etiqueta para mostrar la imagen
        self.label_imagen = tk.Label(self, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=0, column=0, columnspan=1, padx=1, pady=10, sticky="w")

        # Crear un frame para los botones
        button_frame = tk.Frame(self, bg=self.cget('bg'))  # Crea un marco para los botones
        button_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        # Botones
        tk.Button(button_frame, text="Turnos", font=("Calibri", 15),width=8, command=self.abrir_gestion_turnos).grid(row=0, column=0, padx=30)
        tk.Button(button_frame, text="Personas", font=("Calibri", 15),width=8, command=self.personas).grid(row=0, column=1, padx=30)
        tk.Button(button_frame, text="Stock", font=("Calibri", 15),width=8 ,command=self.stock).grid(row=0, column=2, padx=30)
        tk.Button(button_frame, text="Servicios", font=("Calibri", 15),width=8, command=self.servicios).grid(row=0, column=3, padx=30)

    def abrir_gestion_turnos(self):
        iniciar_turnero()

    def personas(self):
        ventana_personas = Toplevel(self)
        ventana_personas.title("Visualizar Personas") 
        ventana_personas.resizable(False, False)  # Deshabilitar el redimensionamiento
        ViewPersonas(ventana_personas)  # Crear la instancia de ViewPersonas
        

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
