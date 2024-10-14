import tkinter as tk
from tkinter import LabelFrame, Entry, Button, StringVar, PhotoImage
from tkinter.ttk import Combobox 
from conexionbd import conectar_bd 

# Ventana
class AltaPersona(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alta de Turnos") 
        self.geometry("1110x510")
        self.configure(bg="#40E0D0")
        self.resizable(False, False)
        ruta_imagen = 'C:/Users/ramye/Desktop/Facultad/Programación 2do año/Interfaces_Peluqueria/imagen3.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        #C:\Users\ramye\Desktop\Facultad\Programación 2do año\Interfaces_Peluqueria
        self.label_imagen = tk.Label(self, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=2, column=4, rowspan=3, padx=20, pady=10)

        # Marco
        frame_datos = LabelFrame(self, text="Ingrese los datos:", bg="#48D1CC", font=('Calibri', 20), borderwidth=5)
        frame_datos.grid(row=1, column=0, columnspan=9, ipady=10)

        # Etiquetas
        label_nombre = tk.Label(frame_datos, text="Nombre: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_nombre.grid(row=1, column=1, pady=10)

        label_apellido = tk.Label(frame_datos, text="DNI: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_apellido.grid(row=2, column=1, pady=10)

        label_dni = tk.Label(frame_datos, text="Servicio: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_dni.grid(row=3, column=1, pady=10)

        label_contacto = tk.Label(frame_datos, text="Contacto: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_contacto.grid(row=4, column=1, pady=10)

        label_tipo = tk.Label(frame_datos, text="Tipo: ", bg="#48D1CC", fg="black", font=('Calibri', 15))
        label_tipo.grid(row=5, column=1, pady=10)

        # Entradas
        entry_nombre = Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_nombre.grid(row=1, column=2, ipadx=400)

        entry_apellido = Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_apellido.grid(row=2, column=2, ipadx=400)

        entry_dni = Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_dni.grid(row=3, column=2, ipadx=400)

        entry_contacto = Entry(frame_datos, bg="white", font=('Calibri', 15))
        entry_contacto.grid(row=4, column=2, ipadx=400)

        # Combobox para seleccionar Servicio
        tipo_var = StringVar(self)
        tipo_combobox = Combobox(frame_datos, textvariable=tipo_var, state="readonly", font=('Calibri', 15))
        tipo_combobox['values'] = ("Cliente", "Empleado")  # VER DE LLAMAR LAS OPCIONES DESDE LA BASE DE DATOS.
        tipo_combobox.set("")  
        tipo_combobox.grid(row=5, column=2, ipadx=390)

        # Botón de Envío
        btn_guardar = Button(frame_datos, text="Guardar", command=self.guardar_datos, bg="light grey", font=('Calibri', 15))
        btn_guardar.grid(row=9, column=1, columnspan=2, pady=20)
        btn_guardar = Button(frame_datos, text="Limpiar", command=self.guardar_datos, bg="light grey", font=('Calibri', 15))
        btn_guardar.grid(row=9, column=2, columnspan=2, pady=20)
    def guardar_datos(self):
        print("Datos guardados")  

if __name__ == "__main__":
    app = AltaPersona()
    app.mainloop()
