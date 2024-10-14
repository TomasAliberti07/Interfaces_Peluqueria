import tkinter as tk
from tkinter import PhotoImage, Toplevel
from viewpersonas import ViewPersonas  # Importamos la clase ViewPersonas

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("860x450")
        self.resizable(False, False)
        self.configure(bg="#40E0D0")
        self.title("Menu")

        ruta_imagen = 'C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen4.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        
        self.label_imagen = tk.Label(self, image=self.imagen,bg=self.cget('bg'))
        self.label_imagen.grid(row=1, column=3, rowspan=5, padx=20, pady=20, sticky="n")

        tk.Button(self, text="Turnos", font=("Calibri", 30), command=self.turnos).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Personas", font=("Calibri", 30), command=self.personas).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self, text="Stock", font=("Calibri", 30), command=self.stock).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self, text="Servicios", font=("Calibri", 30), command=self.servicios).grid(row=4, column=1, padx=10, pady=10)

    def turnos(self):
        ventana_turnos = Toplevel(self)
        ventana_turnos.title("Turnos")
        # Aquí puedes agregar contenido a la ventana de turnos

    def personas(self):
        ventana_personas = Toplevel(self)
        ventana_personas.title("Visualizar Personas")
        ventana_personas.geometry("1366x768")  # Establecer un tamaño adecuado
        ventana_personas.resizable(False, False)  # Deshabilitar el redimensionamiento
        ViewPersonas(ventana_personas)  # Crear la instancia de ViewPersonas  # Creamos una instancia de ViewPersonas y la mostramos

    def stock(self):
        ventana_stock = Toplevel(self)
        ventana_stock.title("Stock")
        # Aquí puedes agregar contenido a la ventana de stock

    def servicios(self):
        ventana_servicios = Toplevel(self)
        ventana_servicios.title("Servicios")
        # Aquí puedes agregar contenido a la ventana de servicios

if __name__ == "__main__":
    menu = Menu()
    menu.mainloop()