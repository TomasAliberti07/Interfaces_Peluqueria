import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  
from Menu import Menu
from conexionbd import conectar_db
import mysql.connector  # Agregué esta línea

class Sesion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")  
        self.resizable(False, False)
        self.configure(bg="#40E0D0")  
        self.title("Inicio de Sesión")

        
        ruta_imagen = 'C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen3.png'
        self.imagen = PhotoImage(file=ruta_imagen)
        
        self.label_imagen = tk.Label(self, image=self.imagen,bg=self.cget('bg'))
        self.label_imagen.grid(row=2, column=1, rowspan=3, padx=20, pady=40)
        
        self.etiqueta1 = tk.Label(self, text="Usuario", font=("Calibri", 20), bg=self.cget('bg'), fg="black")
        self.etiqueta1.grid(row=0, column=0, padx=20, pady=20)
        self.etiqueta2 = tk.Label(self, text="Contraseña", font=("Calibri", 20), bg=self.cget('bg'), fg="black")
        self.etiqueta2.grid(row=1, column=0, padx=20, pady=20)

        
        self.mostrador_usuario = tk.Entry(self, state="normal", font=("Calibri", 15))
        self.mostrador_usuario.grid(row=0, column=1, padx=20, pady=20)
        self.mostrador_contraseña = tk.Entry(self, show="*", state="normal", font=("Calibri", 15))
        self.mostrador_contraseña.grid(row=1, column=1, padx=20, pady=20)

        
        self.boton = tk.Button(self, text="Ingresar", command=self.verificar_sesion, font=("Calibri", 12))
        self.boton.grid(row=2, column=1, padx=10, pady=1)

    def conectar_db(self):  # Agregado self
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",  # PONER SU PROPIO USUARIO
                password="123",  # PONER SU PROPIA CLAVE
                database="base_peluqueria"
            )
            cursor = mydb.cursor()
            return mydb, cursor
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            return None
            
    def verificar_sesion(self):
        try:
            # Obtener la conexión y el cursor
            conexion = self.conectar_db()

            if conexion is None:
                print("No se pudo conectar a la base de datos.")
                return

            mydb, cursor = conexion

            # Obtener los datos de inicio de sesión
            nombre_usuario = self.mostrador_usuario.get()
            contraseña = self.mostrador_contraseña.get()
            print(f"Intentando iniciar sesión con usuario: {nombre_usuario}")

            if isinstance(mydb, mysql.connector.MySQLConnection):
                cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s", (nombre_usuario, contraseña))
                result = cursor.fetchone()

                if result:
                    print("Inicio de sesión exitoso")
                    self.abrir_menu_principal()
                else:
                    print("Credenciales incorrectas")
                    messagebox.showerror("Error", "Credenciales incorrectas")

            cursor.close()
            mydb.close()
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def abrir_menu_principal(self):
        self.destroy()  # Cierra la ventana de inicio de sesión
        menu = Menu()  # Abre el menú principal desde el otro archivo
        menu.mainloop()

ventana = Sesion()
ventana.mainloop()
