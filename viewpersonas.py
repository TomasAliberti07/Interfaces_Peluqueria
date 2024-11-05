import tkinter as tk
import re
from tkinter import ttk, PhotoImage, messagebox
import mysql.connector
class ViewPersonas(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,bg="#40E0D0")
        self.master = master
  
        self.grid_propagate(False)  # Evita que el frame cambie de tamaño
        self.grid(row=0, column=0, sticky="nsew")
        ruta_imagen = 'C:/Users/lauta/OneDrive/Desktop/Facultad/Interfaces_Peluqueria/imagen3.png'
        self.imagen = PhotoImage(file=ruta_imagen) 
        self.master.attributes('-fullscreen', True)  # Modo pantalla completa
        self.pack(fill=tk.BOTH, expand=True)
        self.label_imagen = tk.Label(self, image=self.imagen, bg=self.cget('bg'))
        self.label_imagen.grid(row=4, column=0, rowspan=3, padx=20, pady=10)


        # Conectar a la base de datos y crear un cursor
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto por tu usuario
            password="123",  # Cambia esto por tu contraseña
            database="base_peluqueria"  # Cambia esto por tu base de datos
        )
        self.mycursor = self.mydb.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Frame de búsqueda
        search_frame = tk.LabelFrame(self, text="Buscar por DNI", bg="#40E0D0", font=('Calibri', 20), borderwidth=5)
        search_frame.grid(row=0, column=0, padx=120, pady=20, sticky="ew")

        # Entrada de búsqueda
        self.search_entry = tk.Entry(search_frame, width=20, font=('Calibri', 15))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botones de acción
        search_button = tk.Button(search_frame, text="Buscar", command=self.search_personas, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=1, padx=10, pady=10)
        
        search_button = tk.Button(search_frame, text="+ Agregar", command=self.abrir_altap, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=2, padx=10, pady=10)

        search_button = tk.Button(search_frame, text="Modificar", command=self.modificar_persona, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=3, padx=10, pady=10)
        
        search_button = tk.Button(search_frame, text="Eliminar", command=self.eliminar_persona, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=4, padx=10, pady=10)

        search_button = tk.Button(search_frame, text="Actualizar", command=self.actualizar_persona, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=5, padx=10, pady=10)

        back_button = tk.Button(self, text="Volver", command=self.volver_menu, bg="#ffffff", font=('Calibri', 15), width=8)
        back_button.grid(row=2, column=0, padx=10, pady=10)
    
        

        style = ttk.Style()
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#ffffff")
        
        frame_treeview = tk.Frame(self)
        frame_treeview.grid(row=1, column=0, sticky="nsew", padx=130, pady=0)

    
        self.grid_rowconfigure(1, weight=1)  # Permitir que la fila 1 (donde está el frame_treeview) se expanda
        self.grid_columnconfigure(0, weight=1)  # Permitir que la columna 0 (donde está el frame_treeview) se expanda

    # Treeview de personas
        self.personas_treeview = ttk.Treeview(frame_treeview, columns=("dni", "nombre", "apellido", "contacto", "correo", "tipo", "activo", "id_tipo_p"), show="headings")
        self.personas_treeview.grid(row=0, column=0, sticky="nsew")  

    
        frame_treeview.grid_rowconfigure(0, weight=1)  # Permitir que la fila del Treeview se expanda
        frame_treeview.grid_columnconfigure(0, weight=1)  # Permitir que la columna del Treeview se expanda

    # Configuración del Treeview
        self.personas_treeview.heading("nombre", text="Nombre")
        self.personas_treeview.heading("apellido", text="Apellido")
        self.personas_treeview.heading("dni", text="DNI")
        self.personas_treeview.heading("contacto", text="Contacto")
        self.personas_treeview.heading("correo", text="Correo")
        self.personas_treeview.heading("tipo", text="Tipo")
        self.personas_treeview.heading("activo", text="Activo")
        self.personas_treeview.heading("id_tipo_p", text="Tipo ID")

    # Ancho de las columnas y datos centrados
        self.personas_treeview.column("nombre", anchor='center', width=150)
        self.personas_treeview.column("apellido", anchor='center', width=150)
        self.personas_treeview.column("dni", anchor='center', width=150)
        self.personas_treeview.column("contacto", anchor='center', width=150)
        self.personas_treeview.column("correo", anchor='center', width=150)
        self.personas_treeview.column("tipo", anchor='center', width=150)
        self.personas_treeview.column("activo", anchor='center', width=100)
        self.personas_treeview.column("id_tipo_p", anchor='center', width=100)

    # Scrollbar
        self.scrollbar = tk.Scrollbar(frame_treeview, orient="vertical", command=self.personas_treeview.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')  # Colocar el scrollbar a la derecha del Treeview

    # Configurar el Treeview para que use el scrollbar
        self.personas_treeview.configure(yscrollcommand=self.scrollbar.set)

    # Permitir que el Treeview ocupe todo el espacio del frame
        frame_treeview.grid_rowconfigure(0, weight=1)  # Permitir que la fila del Treeview se expanda
        frame_treeview.grid_columnconfigure(0, weight=1)

        # Carga los datos iniciales
        self.load_personas()

    def load_personas(self):
        self.mycursor.execute("SELECT * FROM persona WHERE activo = 'si'")  # Filtrar solo activos
        personas = self.mycursor.fetchall()
        self.personas_treeview.delete(*self.personas_treeview.get_children())  # Limpiar el Treeview antes de cargar
        for persona in personas:
            values = (persona[3], persona[1], persona[2], persona[4], persona[9], persona[5], persona[6], persona[7])
            self.personas_treeview.insert("", "end", values=values)

    def search_personas(self):
      dni = self.search_entry.get()

      if not dni:  
        messagebox.showwarning("Advertencia", "Debe ingresar un DNI para buscar a una persona.")
        return 

      if not dni.isdigit():
        messagebox.showwarning("Advertencia", "Debe ingresar un DNI válido.")
        return  
      
      self.mycursor.execute("SELECT * FROM persona WHERE dni LIKE %s", (dni+"%",))
      personas = self.mycursor.fetchall()

      self.personas_treeview.delete(*self.personas_treeview.get_children())
    
      for persona in personas:
        values = (persona[3], persona[1], persona[2], persona[4], persona[9], persona[5], persona[6], persona[7])
        self.personas_treeview.insert("", "end", values=values)
      


    def actualizar_persona(self):
        self.mycursor.execute("SELECT * FROM persona WHERE activo = 'si'")
        personas = self.mycursor.fetchall()
        self.personas_treeview.delete(*self.personas_treeview.get_children())
        for persona in personas:
         values = (persona[3], persona[1], persona[2], persona[4], persona[9], persona[5], persona[6], persona[7])
         self.personas_treeview.insert("", "end", values=values)


    def modificar_persona(self):
        selected_item = self.personas_treeview.selection()  # Obtiene el item seleccionado
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una persona para modificar.")
            return  

        persona_dni = self.personas_treeview.item(selected_item, 'values')[0]  # Obtiene el DNI del item seleccionado
        self.mycursor.execute("SELECT * FROM persona WHERE dni = %s", (persona_dni,))
        persona = self.mycursor.fetchone()  #Datos de persona

        if persona:
            ModificarPersona(self, persona)  # Abrir la ventana de modificación
        else:
            messagebox.showerror("Error", "Persona no encontrada.")
        

    def eliminar_persona(self): 
        selected_item = self.personas_treeview.selection()  
        if not selected_item:  # Verifica si no hay selección
            messagebox.showwarning("Advertencia", "Por favor, selecciona una persona para eliminar.")  
            return  

        persona_dni = self.personas_treeview.item(selected_item, 'values')[0]  
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar a la persona con DNI {persona_dni}?")
        if confirm:
            self.mycursor.execute("UPDATE persona SET activo = 'no' WHERE dni = %s", (persona_dni,))
            self.mydb.commit()  #
           
        self.load_personas() 
    def abrir_altap(self):
        from alta_persona2 import AltaPersona
        alta = AltaPersona(self)  
        alta.transient(self)  
        alta.grab_set()
        
    def volver_menu(self):
          # Muestra el menú principal
        self.destroy()  
       
class ModificarPersona:
    def __init__(self, parent, persona):
        self.parent = parent
        self.persona = persona

        # Crear la ventana de modificación
        self.window = tk.Toplevel(parent.master)
        self.window.title("Modificar Persona")
        self.window.geometry("400x500")
        self.window.resizable(False,False)
        self.window.configure(bg="#40E0D0")
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.create_widgets()
    def volver(self):
           self.window.destroy()
    def create_widgets(self):

        tk.Label(self.window, text="Dni:", bg="#40E0D0").pack(pady=5)
        self.dni_entry = tk.Entry(self.window)
        self.dni_entry.insert(0, self.persona[3])  # Cargar el nombre actual
        self.dni_entry.pack(pady=5)
        
        tk.Label(self.window, text="Nombre:", bg="#40E0D0").pack(pady=5)
        self.nombre_entry = tk.Entry(self.window)
        self.nombre_entry.insert(0, self.persona[1])  # Cargar el nombre actual
        self.nombre_entry.pack(pady=5)

        tk.Label(self.window, text="Apellido:", bg="#40E0D0").pack(pady=5)
        self.apellido_entry = tk.Entry(self.window)
        self.apellido_entry.insert(0, self.persona[2])  # Cargar el apellido actual
        self.apellido_entry.pack(pady=5)

        tk.Label(self.window, text="Contacto:", bg="#40E0D0").pack(pady=5)
        self.contacto_entry = tk.Entry(self.window)
        self.contacto_entry.insert(0, self.persona[4])  # Cargar el contacto actual
        self.contacto_entry.pack(pady=5)

        tk.Label(self.window, text="Correo:", bg="#40E0D0").pack(pady=5)
        self.correo_entry = tk.Entry(self.window)
        self.correo_entry.insert(0, self.persona[9])  # Cargar el correo actual
        self.correo_entry.pack(pady=5)
        
        tk.Label(self.window, text="Activo:", bg="#40E0D0").pack(pady=5)
        self.activo_var = tk.StringVar(value="1" if self.persona[7] == 1 else "0")  
        self.radio_si = tk.Radiobutton(self.window, text="Sí", variable=self.activo_var, value="1", bg="#40E0D0")
        self.radio_si.pack(pady=5)

        self.activo_var.set("1")  
        
        

        modificar_button = tk.Button(self.window, text="Modificar", command=self.modificar_persona)
        modificar_button.pack(pady=20)
        volver_button = tk.Button(self.window, text="Volver", command=self.volver)
        volver_button.pack(pady=20)
    def campo_vacio_o_espacio(self, texto):
        return not texto.strip()
    
    def validar_dni(self,dni):
    
     if not dni.isdigit(): 
        messagebox.showerror("Error", "Solamente se aceptan dígitos en el dni")
        return False
     elif len(dni) < 7 or len(dni) > 8:  
        messagebox.showerror("Error", "El número del dni debe tener 7 u 8 dígitos")
        return   False   
     return True
    def verificar_correo(self,correo):
   
     patron = r'^[a-zA-ZñÑ0-9._%+-]+@[a-zA-ZñÑ0-9.-]+\.[a-zA-ZñÑ]{2,}$'

    
     if not re.match(patron, correo):
        messagebox.showerror("Error", f"{correo} : no es una dirección de correo válida.")
        return False
     return True
    
    def validar_nombre_apellido(self, nombre, apellido):
      patron = r'^[A-Za-zñÑáéíóúÁÉÍÓÚ ]+$'  
      if not re.match(patron, nombre):
        messagebox.showerror("Error", "El nombre debe contener solo letras.")
        return False
      if not re.match(patron, apellido):
        messagebox.showerror("Error", "El apellido debe contener solo letras.")
        return False
      return True
    
    def validar_telefono(self,contacto):
      if not contacto.isdigit():  
        messagebox.showerror("Error", "Solamente se aceptan dígitos en contacto")
        return False
      elif len(contacto) < 6 or len(contacto) > 10:
        messagebox.showerror("Error", "El número de teléfono debe tener entre 6 y 10 dígitos")
        return False
      return True
            

    def modificar_persona(self):
    # Recoge los datos de las entradas
     nuevo_dni = self.dni_entry.get().strip()  
     nuevo_nombre = self.nombre_entry.get().strip().upper()
     nuevo_apellido = self.apellido_entry.get().strip().upper()
     nuevo_contacto = self.contacto_entry.get().strip()
     nuevo_correo = self.correo_entry.get().strip().upper()

     nuevo_activo = "sí"

    # Validaciones
     if self.campo_vacio_o_espacio(nuevo_dni) or not self.validar_dni(nuevo_dni):
        return  

     if self.campo_vacio_o_espacio(nuevo_nombre) or not self.validar_nombre_apellido(nuevo_nombre, nuevo_apellido):
        return  

     if self.campo_vacio_o_espacio(nuevo_contacto) or not self.validar_telefono(nuevo_contacto):
        return  

     if self.campo_vacio_o_espacio(nuevo_correo) or not self.verificar_correo(nuevo_correo):
        return  

   
     self.parent.mycursor.fetchall()  
     self.parent.mycursor.execute("""
        UPDATE persona SET nombre = %s, apellido = %s, dni = %s, contacto = %s, correo = %s, activo = %s
        WHERE dni = %s
     """, (nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_contacto, nuevo_correo, nuevo_activo, self.persona[3]))  # Usar el DNI original para identificar a la persona

     self.parent.mydb.commit()

     messagebox.showinfo("Éxito", "Persona modificada con éxito.")
     self.parent.load_personas() 
     self.window.destroy()  


if __name__ == "__main__":
    root = tk.Tk()
    app = ViewPersonas(master=root)
    root.title("Consulta Persona")
    root.protocol("WM_DELETE_WINDOW", lambda: None) 
    app.mainloop()
