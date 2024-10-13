import tkinter as tk
from tkinter import LabelFrame, Entry, Button, StringVar, PhotoImage
from tkinter.ttk import Combobox  

# Ventana
class AltaPersona(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alta de persona") 
        self.geometry("1110x380")
        self.configure(bg="#40E0D0")
        self.resizable(False, False)
        ruta_imagen = 'C:/Users/GUILLERMINA/Desktop/Interfaces de la peluqueria/imagen3.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        
        self.label_imagen = tk.Label(self, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=2, column=4, rowspan=3, padx=20, pady=10)

        # Marco
        frame_datos = LabelFrame(self, text="Ingrese los datos:", bg="#48D1CC", font=('Calibri', 20), borderwidth=5)
        frame_datos.grid(row=1, column=0, columnspan=9, ipady=10)

        # Etiquetas
        label_descripcion = tk.Label(frame_datos, text="Descripcion: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_descripcion.grid(row=1, column=1, pady=10)

        label_tiempoestimado = tk.Label(frame_datos, text="Tiempo Estimado: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_tiempoestimado.grid(row=2, column=1, pady=10)
        
        label_precio = tk.Label(frame_datos, text="Precio: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_precio.grid(row=3, column=1, pady=10)
       
        # Entradas
        entry_descripcion = Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_descripcion.grid(row=1, column=2, ipadx=400)

        entry_tiempoestimado= Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_tiempoestimado.grid(row=2, column=2, ipadx=400)
        
        entry_cantidad = Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_cantidad.grid(row=3, column=2, ipadx=400)
        # Botón de Envío
        btn_guardar = Button(frame_datos, text="Guardar", command=self.guardar_datos, bg="light grey", font=('Calibri', 15))
        btn_guardar.grid(row=9, column=1, columnspan=2, pady=20)
        btn_guardar = Button(frame_datos, text="Limpiar", command=self.limpiar_campos, bg="light grey", font=('Calibri', 15))
        btn_guardar.grid(row=9, column=2, columnspan=2, padx=500,pady=20)
    def guardar_datos(self):
        print("Datos guardados")  

    def limpiar_campos( entries):
        for entry in entries:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    app = AltaPersona()
    app.mainloop()
