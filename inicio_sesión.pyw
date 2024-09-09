import tkinter as tk
from tkinter import messagebox  

class Sesion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.usuario = "Tomas"
        self.contraseña = 1234
        self.resizable(False, False)
        self.configure(bg="#AFEEEE")  
        self.title("Inicio de Sesión")

        
        self.etiqueta1 = tk.Label(self, text="Usuario")
        self.etiqueta1.grid(row=0, column=0, padx=10, pady=10)
        self.etiqueta2 = tk.Label(self, text="Contraseña")
        self.etiqueta2.grid(row=1, column=0, padx=10, pady=10)

        
        self.mostrador_usuario = tk.Entry(self,state="normal")
        self.mostrador_usuario.grid(row=0, column=1, padx=10, pady=10)
        self.mostrador_contraseña = tk.Entry(self, show="*", state="normal")
        self.mostrador_contraseña.grid(row=1, column=1, padx=10, pady=10)

        
        self.boton = tk.Button(self, text="Ingresar", command=self.verificar_sesion)
        self.boton.grid(row=2, column=1, padx=10, pady=10)

    
    def verificar_sesion(self):
        usuario_ingresado = self.mostrador_usuario.get()
        contraseña_ingresada = self.mostrador_contraseña.get()

        if usuario_ingresado == self.usuario and int(contraseña_ingresada) == self.contraseña:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")  
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")  


ventana = Sesion()
ventana.mainloop()
