import tkinter as tk
from tkinter import PhotoImage  


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("860x450")
        self.resizable(False, False)
        self.configure(bg="#40E0D0")
        self.title("Menu")


        ruta_imagen = 'C:/Users/GUILLERMINA/Desktop/Interfaces de la peluqueria/imagen4.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        
        self.label_imagen = tk.Label(self, image=self.imagen,bg=self.cget('bg'))
        self.label_imagen.grid(row=1, column=3, rowspan=5, padx=20, pady=20, sticky="n")


        tk.Button(self, text="Turnos", font=("Calibri", 30)).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Personas", font=("Calibri", 30)).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self, text="Stock", font=("Calibri", 30)).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self, text="Servicios", font=("Calibri", 30)).grid(row=4, column=1, padx=10, pady=10)


if __name__ == "__main__":
    menu = Menu()
    menu.mainloop()
