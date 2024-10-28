import os
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Toplevel
from conexionbd import conectar_db
from alta_producto import AltaProducto

class ListadoProductos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Listado de Productos")
        self.geometry("1300x600")

        # Establecer fondo
        self.configure(bg="#40E0D0")

        # Frame para la fila de botones
        self.frame_botones = tk.Frame(self, bg="#40E0D0")
        self.frame_botones.pack(fill=tk.X, pady=10)

        # Botón buscar y campo de entrada
        self.entry_buscar = tk.Entry(self.frame_botones)
        self.entry_buscar.pack(side=tk.LEFT, padx=10)
        self.boton_buscar = tk.Button(self.frame_botones, text="Buscar", command=self.buscar_producto)
        self.boton_buscar.pack(side=tk.LEFT, padx=10)
        
        # Botón modificar
        self.boton_modificar = tk.Button(self.frame_botones, text="Modificar Producto", command=self.modificar_producto)
        self.boton_modificar.pack(side=tk.LEFT, padx=10)
        
        # Botón eliminar
        self.boton_eliminar = tk.Button(self.frame_botones, text="Eliminar Producto", command=self.eliminar_producto)
        self.boton_eliminar.pack(side=tk.RIGHT, padx=10)

        # Botón agregar producto 
        self.boton_agregar = tk.Button(self.frame_botones, text="Agregar Producto", command=self.abrir_alta_producto)
        self.boton_agregar.pack(side=tk.LEFT, padx=10)

        # Botón para volver al menú
        boton_volver = tk.Button(self.frame_botones, text="Volver", command=self.volver_menu)
        boton_volver.pack(side=tk.RIGHT, padx=5)
        
        # Crear Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "nombre", "marca", "cantidad", "precio"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("marca", text="Marca")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        
        self.tree.column("ID", width=50)
        self.tree.column("nombre", width=150)
        self.tree.column("marca", width=100)
        self.tree.column("cantidad", width=100)
        self.tree.column("precio", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.frame_modificar = tk.Frame(self, bg="#40E0D0")
        self.frame_modificar.pack(pady=10)
        
        label_nombre = tk.Label(self.frame_modificar, text="Nombre:", bg="#40E0D0")
        label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(self.frame_modificar)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        label_marca = tk.Label(self.frame_modificar, text="Marca:", bg="#40E0D0")
        label_marca.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_marca = tk.Entry(self.frame_modificar)
        self.entry_marca.grid(row=1, column=1, padx=5, pady=5)

        label_cantidad = tk.Label(self.frame_modificar, text="Cantidad:", bg="#40E0D0")
        label_cantidad.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_cantidad = tk.Entry(self.frame_modificar)
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5)

        label_precio = tk.Label(self.frame_modificar, text="Precio:", bg="#40E0D0")
        label_precio.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_precio = tk.Entry(self.frame_modificar)
        self.entry_precio.grid(row=3, column=1, padx=5, pady=5)

        self.boton_guardar = tk.Button(self.frame_modificar, text="Guardar Cambios", command=self.guardar_cambios)
        self.boton_guardar.grid(row=4, columnspan=2)
        
        # Obtener datos de la base de datos
        self.obtener_datos()
    
    def volver_menu(self):
        self.destroy()
        self.master.deiconify()
    
    def abrir_alta_producto(self):
        ventana_alta = AltaProducto(self)
    
    def obtener_datos(self):
        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return
        
        cursor.execute("SELECT id_producto, nombre, marca, cantidad, precio FROM producto")
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        cursor.close()
        mydb.close()
    
    def modificar_producto(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Por favor seleccione un producto")
            return
        
        item = self.tree.item(selected_items[0])
        record = item['values']
        
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, record[1])
        self.entry_marca.delete(0, tk.END)
        self.entry_marca.insert(0, record[2])
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, record[3])
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, record[4])
        
        self.producto_id = record[0]
    
    def guardar_cambios(self):
        if not self.validar_campos():
            return
        
        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return
        
        nombre = self.entry_nombre.get()
        marca = self.entry_marca.get()
        cantidad = int(self.entry_cantidad.get())
        precio = float(self.entry_precio.get())
        
        query = "UPDATE producto SET nombre=%s, marca=%s, cantidad=%s, precio=%s WHERE id_producto=%s"
        valores = (nombre, marca, cantidad, precio, self.producto_id)
        
        try:
            cursor.execute(query, valores)
            mydb.commit()
            messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            self.limpiar_campos()
            self.tree.delete(*self.tree.get_children())
            self.obtener_datos()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al actualizar los datos: {e}")
        finally:
            cursor.close()
            mydb.close()
    
    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
    
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
        if not precio.replace('.','',1).isdigit():
            messagebox.showerror("Error", "El precio debe ser un número")
            return False
        return True
    
    def buscar_producto(self):
        buscar_texto = self.entry_buscar.get()
        if not buscar_texto:
            messagebox.showerror("Error", "Ingrese un término de búsqueda")
            return
        
        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return
        
        query = "SELECT id_producto, nombre, marca, cantidad, precio FROM producto WHERE nombre LIKE %s OR marca LIKE %s"
        valores = (f"%{buscar_texto}%", f"%{buscar_texto}%")
        
        try:
            cursor.execute(query, valores)
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al buscar los datos: {e}")
        finally:
            cursor.close()
            mydb.close()
    
    def eliminar_producto(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Por favor seleccione un producto")
            return
        
        item = self.tree.item(selected_items[0])
        producto_id = item['values'][0]
        
        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return
        
        query = "DELETE FROM producto WHERE id_producto=%s"
        valores = (producto_id,)
        
        try:
            cursor.execute(query, valores)
            mydb.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            self.tree.delete(selected_items[0])
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el producto: {e}")
        finally:
            cursor.close()
            mydb.close()
    

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    app = ListadoProductos(master=root)
    app.mainloop()