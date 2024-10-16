import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.simpledialog
from tkcalendar import Calendar, DateEntry

class AltaTurno:
    def __init__(self, master):
        self.master = master
        master.title("Alta de Turno")
        master.configure(bg="#40E0D0")
        master.geometry("800x600")  # Aumenta el tamaño de la ventana

        # Cargar y mostrar logo
        self.logo = Image.open("C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen4.png")
        self.logo = self.logo.resize((200, 200), Image.Resampling.LANCZOS)  # Aumenta el tamaño del logo
        self.logo_img = ImageTk.PhotoImage(self.logo)
        tk.Label(master, image=self.logo_img, bg="#f0f0f0").grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Crear etiquetas y entradas
        tk.Label(master, text="Fecha del turno:", bg="#f0f0f0", font=("Arial", 18)).grid(row=1, column=0, padx=20, pady=20)  # Aumenta el tamaño de la fuente
        self.fecha_turno = tk.Entry(master, width=30, font=("Arial", 18))  # Aumenta el tamaño de la entrada
        self.fecha_turno.grid(row=1, column=1, padx=20, pady=20)

        # Botón para seleccionar fecha
        tk.Button(master, text="Seleccionar fecha", command=self.seleccionar_fecha, bg="#008CBA", fg="white", font=("Arial", 18)).grid(row=1, column=2, padx=20, pady=20)

        tk.Label(master, text="Hora del turno:", bg="#f0f0f0", font=("Arial", 18)).grid(row=2, column=0, padx=20, pady=20)
        
        # Label con los dos puntos (:) entre los Spinbox
        tk.Label(master, text=":", font=("Arial", 18)).grid(row=2, column=1, padx=(60, 0), pady=20)
        
        # Crear Spinbox para horas
        self.hora_turno = tk.Spinbox(master, from_=0, to=23, width=5, font=("Arial", 18), format="%02.0f")
        self.hora_turno.grid(row=2, column=1, padx=(20, 0), pady=20)

        # Crear Spinbox para minutos
        self.minuto_turno = tk.Spinbox(master, from_=0, to=59, width=5, font=("Arial", 18), format="%02.0f")
        self.minuto_turno.grid(row=2, column=2, padx=(80, 0), pady=20)

    
        # Crear botón para registrar turno
        tk.Button(master, text="Registrar turno", command=self.registrar_turno, bg="#008CBA", fg="white", font=("Arial", 18)).grid(row=3, column=1, padx=20, pady=30)  # Aumenta el tamaño del botón

    def seleccionar_fecha(self):
        # Abrir calendario para seleccionar fecha
        def get_date():
            selected_date = cal.selection_get()
            self.fecha_turno.delete(0, tk.END)
            self.fecha_turno.insert(0, selected_date.strftime("%Y-%m-%d"))
            top.destroy()

        top = tk.Toplevel(self.master)
        top.title("Seleccionar fecha")
        cal = Calendar(top, selectmode='day', year=2023, month=10, day=1)
        cal.pack(pady=20)
        tk.Button(top, text="Seleccionar", command=get_date, font=("Arial", 18)).pack(pady=10)  # Aumenta el tamaño del botón

    def registrar_turno(self):
        # Obtener valores de las entradas
        fecha_turno = self.fecha_turno.get()
        hora_turno = self.hora_turno.get()
        minuto_turno = self.minuto_turno.get()

        # Validar y mostrar la hora y minutos
        hora_minuto = f"{hora_turno}:{minuto_turno}"
        messagebox.showinfo("Turno registrado", f"Turno registrado para el {fecha_turno} a las {hora_minuto}")


root = tk.Tk()
alta_turno = AltaTurno(root)
root.mainloop()