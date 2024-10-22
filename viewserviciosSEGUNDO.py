import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class ViewServicios(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#40E0D0", width=1280, height=720)
        self.master = master
        self.grid_propagate(False)
        self.grid(row=0, column=0, sticky="nsew")

        # Conectar a la base de datos y crear un cursor
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="base_peluqueria"
        )
        self.mycursor = self.mydb.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Frame de búsqueda
        search_frame = tk.LabelFrame(self, text="Buscar por nombre", bg="#40E0D0", font=('Calibri', 20), borderwidth=5)
        search_frame.grid(row=0, column=0, padx=10, pady=20, sticky="w")

        # Entrada de búsqueda
        self.search_entry = tk.Entry(search_frame, width=20, font=('Calibri', 15))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Botón de búsqueda
        search_button = tk.Button(search_frame, text="Buscar", command=self.search_servicios, bg="#ffffff", font=('Calibri', 15), width=8)
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Botón de agregar
        add_button = tk.Button(search_frame, text="+Agregar", command=self.abrir_alta, bg="#ffffff", font=('Calibri', 15), width=8)
        add_button.grid(row=0, column=2, padx=10, pady=10)

        # Botón de eliminar
        delete_button = tk.Button(search_frame, text="Eliminar", command=self.delete_servicio, bg="#ffffff", font=('Calibri', 15), width=8)
        delete_button.grid(row=0, column=3, padx=10, pady=10)

        # Botón de modificar
        modify_button = tk.Button(search_frame, text="Modificar", command=self.modify_servicio, bg="#ffffff", font=('Calibri', 15), width=8)
        modify_button.grid(row=0, column=4, padx=10, pady=10)

        # Botón Volver
        back_button = tk.Button(search_frame, text="Volver", command=self.volver_menu, bg="#ffffff", font=('Calibri', 15), width=8)
        back_button.grid(row=0, column=5, padx=10, pady=10)

        # Treeview de servicios
        self.servicios_treeview = ttk.Treeview(self, columns=("nombre", "descripcion", "Tiempo Estimado"), show="headings")
        self.servicios_treeview.grid(row=1, column=0, sticky="w", padx=130, pady=10)

        # Configuración del Treeview
        self.servicios_treeview.heading("nombre", text="Nombre")
        self.servicios_treeview.heading("descripcion", text="Descripción")
        self.servicios_treeview.heading("Tiempo Estimado", text="Tiempo Estimado")

        # Ancho de las columnas y datos centrados
        self.servicios_treeview.column("nombre", anchor='center', width=150)
        self.servicios_treeview.column("descripcion", anchor='center', width=200)
        self.servicios_treeview.column("Tiempo Estimado", anchor='center', width=100)

        # Carga los servicios
        self.load_servicios()

    def load_servicios(self):
        self.mycursor.execute("SELECT * FROM servicio")
        servicios = self.mycursor.fetchall()
        self.servicios_treeview.delete(*self.servicios_treeview.get_children())
        for servicio in servicios:
            self.servicios_treeview.insert("", "end", values=(servicio[3], servicio[1], servicio[2]))

    def search_servicios(self):
        nombre = self.search_entry.get()
        if nombre:
            self.mycursor.execute("SELECT * FROM servicio WHERE nombre = %s", (nombre,))
            servicios = self.mycursor.fetchall()
            self.servicios_treeview.delete(*self.servicios_treeview.get_children())
            for servicio in servicios:
                self.servicios_treeview.insert("", "end", values=(servicio[3], servicio[1], servicio[2]))

    def delete_servicio(self):
        selected_item = self.servicios_treeview.selection()
        if selected_item:
            servicio_nombre = self.servicios_treeview.item(selected_item, 'values')[0]
            self.mycursor.execute("DELETE FROM servicio WHERE nombre = %s", (servicio_nombre,))
            self.mydb.commit()
            self.servicios_treeview.delete(selected_item)
            messagebox.showinfo("Éxito", "Servicio eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un servicio para eliminar.")

    def modify_servicio(self):
        selected_item = self.servicios_treeview.selection()
        if selected_item:
            servicio_nombre = self.servicios_treeview.item(selected_item, 'values')[0]
            # Abrir un cuadro de diálogo para modificar el servicio
            self.open_modify_dialog(servicio_nombre)
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un servicio para modificar.")

    def open_modify_dialog(self, servicio_nombre):
        # Obtener los detalles del servicio seleccionado
        self.mycursor.execute("SELECT * FROM servicio WHERE nombre = %s", (servicio_nombre,))
        servicio = self.mycursor.fetchone()

        # Crear una nueva ventana para modificar el servicio
        modify_window = tk.Toplevel(self)
        modify_window.title("Modificar Servicio")
        modify_window.geometry("400x300")

        tk.Label(modify_window, text="Nombre:", font=('Calibri', 12)).pack(pady=10)
        nombre_entry = tk.Entry(modify_window, font=('Calibri', 12))
        nombre_entry.insert(0, servicio[3])  # nombre
        nombre_entry.pack(pady=10)

        tk.Label(modify_window, text="Descripción:", font=('Calibri', 12)).pack(pady=10)
        descripcion_entry = tk.Entry(modify_window, font=('Calibri', 12))
        descripcion_entry.insert(0, servicio[1])  # descripción
        descripcion_entry.pack(pady=10)

        tk.Label(modify_window, text="Tiempo Estimado:", font=('Calibri', 12)).pack(pady=10)
        tiempo_entry = tk.Entry(modify_window, font=('Calibri', 12))
        tiempo_entry.insert(0, servicio[2])  # tiempo estimado
        tiempo_entry.pack(pady=10)

        def save_changes():
            nuevo_nombre = nombre_entry.get()
            nueva_descripcion = descripcion_entry.get()
            nuevo_tiempo = tiempo_entry.get()

            # Validar que no exista un servicio con el mismo nombre
            self.mycursor.execute("SELECT * FROM servicio WHERE nombre = %s", (nuevo_nombre,))
            if self.mycursor.fetchone() and nuevo_nombre != servicio[3]:
                messagebox.showwarning("Advertencia", "El servicio ya existe con ese nombre.")
                return

            # Actualizar el servicio en la base de datos
            self.mycursor.execute("UPDATE servicio SET nombre = %s, descripcion = %s, tiempo_estimado = %s WHERE nombre = %s",
                                  (nuevo_nombre, nueva_descripcion, nuevo_tiempo, servicio[3]))
            self.mydb.commit()
            modify_window.destroy()
            self.load_servicios()
            messagebox.showinfo("Éxito", "Servicio modificado correctamente.")

        save_button = tk.Button(modify_window, text="Guardar Cambios", command=save_changes)
        save_button.pack(pady=20)

    def abrir_alta(self):
        alta_window = tk.Toplevel(self)
        alta_window.title("Agregar Servicio")
        alta_window.geometry("400x300")

        tk.Label(alta_window, text="Nombre:", font=('Calibri', 12)).pack(pady=10)
        nombre_entry = tk.Entry(alta_window, font=('Calibri', 12))
        nombre_entry.pack(pady=10)

        tk.Label(alta_window, text="Descripción:", font=('Calibri', 12)).pack(pady=10)
        descripcion_entry = tk.Entry(alta_window, font=('Calibri', 12))
        descripcion_entry.pack(pady=10)

        tk.Label(alta_window, text="Tiempo Estimado:", font=('Calibri', 12)).pack(pady=10)
        tiempo_entry = tk.Entry(alta_window, font=('Calibri', 12))
        tiempo_entry.pack(pady=10)

        def agregar_servicio():
            nombre = nombre_entry.get()
            descripcion = descripcion_entry.get()
            tiempo_estimado = tiempo_entry.get()

            # Validar que no exista un servicio con el mismo nombre
            self.mycursor.execute("SELECT * FROM servicio WHERE nombre = %s", (nombre,))
            if self.mycursor.fetchone():
                messagebox.showwarning("Advertencia", "El servicio ya existe.")
                return
            # Agregar el nuevo servicio
            self.mycursor.execute("INSERT INTO servicio (nombre, descripcion, tiempo_estimado) VALUES (%s, %s, %s)",
                                  (nombre, descripcion, tiempo_estimado))
            self.mydb.commit()
            alta_window.destroy()
            self.load_servicios()  # Recargar la lista de servicios
            messagebox.showinfo("Éxito", "Servicio agregado correctamente.")

        add_button = tk.Button(alta_window, text="Agregar Servicio", command=agregar_servicio)
        add_button.pack(pady=20)

    def volver_menu(self):
        # Aquí puedes implementar la lógica para regresar al menú principal
        self.master.destroy()  # Esto cierra la ventana actual

    def __del__(self):
        self.mycursor.close()
        self.mydb.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Listado de servicios")
    root.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana
    app = ViewServicios(root)
    app.mainloop()