import mysql.connector
import tkinter as tk
from tkinter import LabelFrame, Entry, Button, messagebox
from conexionbd import conectar_db

class AltaProducto(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Alta de producto")
        self.attributes('-fullscreen', True)
        self.configure(bg="#40E0D0")
        self.resizable(False, False)

        # Marco
        frame_datos = LabelFrame(self, text="Ingrese los datos:", bg="#48D1CC", font=('Calibri', 40), borderwidth=5)
        frame_datos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Etiquetas y campos de entrada
        label_nombre = tk.Label(frame_datos, text="Nombre: ", bg="#48D1CC", fg="black", font=('Calibri', 30))
        label_nombre.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre = tk.Entry(frame_datos, font=('Calibri', 20), width=30) 
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        label_marca = tk.Label(frame_datos, text="Marca: ", bg="#48D1CC", fg="black", font=('Calibri', 30))
        label_marca.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_marca = tk.Entry(frame_datos, font=('Calibri', 20), width=30) 
        self.entry_marca.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        label_cantidad = tk.Label(frame_datos, text="Cantidad: ", bg="#48D1CC", fg="black", font=('Calibri', 30))
        label_cantidad.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_cantidad = tk.Entry(frame_datos, font=('Calibri', 20), width=30)  
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        label_precio = tk.Label(frame_datos, text="Precio: ", bg="#48D1CC", fg="black", font=('Calibri', 30))
        label_precio.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_precio = tk.Entry(frame_datos, font=('Calibri', 20), width=30)  
        self.entry_precio.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        
        frame_datos.grid_columnconfigure(1, weight=1)

        # Botones
        frame_botones = tk.Frame(self, bg="#40E0D0")
        frame_botones.grid(row=1, column=0, pady=10, sticky="ew")

        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)
        frame_botones.grid_columnconfigure(2, weight=1)
        frame_botones.grid_columnconfigure(3, weight=1)

        boton_guardar = tk.Button(frame_botones, text="Guardar", font=('calibri', 20), command=self.guardar_datos, padx=10, pady=5) 
        boton_guardar.grid(row=0, column=1, padx=5)

        boton_limpiar = tk.Button(frame_botones, text="Limpiar", font=('calibri', 20), command =self.limpiar_campos, padx=10, pady=5) 
        boton_limpiar.grid(row=0, column=2, padx=5)

        boton_volver = tk.Button(frame_botones, text="Volver", font=('calibri', 20), command=self.destroy, padx=10, pady=5)  
        boton_volver.grid(row=0, column=3, padx=5, sticky="e")

        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def validar_campos(self):
        nombre = self.entry_nombre.get()
        marca = self.entry_marca.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()

        if nombre == "" or marca == "" or cantidad == "" or precio == "":
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return False
        if not cantidad.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return False
        if not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "El precio debe ser un número")
            return False
        return True

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def guardar_datos(self):
        if not self.validar_campos():
            return

        cnx, cursor = conectar_db()
        if cnx is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return
        nombre = self.entry_nombre.get().upper()
        marca = self.entry_marca.get().upper()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()
    
        query = "INSERT INTO producto (nombre, marca, cantidad, precio) VALUES (%s, %s, %s, %s)"
        valores = (nombre, marca, cantidad, precio)
        try:
            cursor.execute(query, valores)
            cnx.commit()
            messagebox.showinfo("Éxito", "Datos guardados")
            self.limpiar_campos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al guardar los datos: {err}")
        finally:
            cursor.close()
            cnx.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = AltaProducto(root)
    root.mainloop()