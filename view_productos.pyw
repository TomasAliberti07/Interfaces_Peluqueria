import tkinter as tk
from tkinter import ttk,messagebox
from conexionbd import conectar_db
import mysql.connector
    #cursor= cnx.cursor()
   # return cnx,cursor

class ListadoProductos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Listado de Productos")
        self.geometry("1300x400")
        
        # Conectar a la base de datos
        #mydb,cursor = conectar_db()

          
        #ytreeview
        self.tree = ttk.Treeview(self, columns=("ID", "nombre", "marca", "cantidad", "precio"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("nombre", text="nombre")
        self.tree.heading("marca", text="marca")
        self.tree.heading("cantidad", text="cantidad")
        self.tree.heading("precio", text="precio")
        self.tree.pack(fill=tk.BOTH, expand=True)

        #Boton modificar
        self.btn_modificar = tk.Button(self, text="Modificar", command=self.modificar_producto)
        self.btn_modificar.pack(pady=10)

        #modificar las entradas
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()
        self.entry_cantidad = tk.Entry(self)
        self.entry_cantidad.pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()
        self.btn_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos)
        self.btn_guardar.pack(pady=10)

        #boton buscar
        self.boton_buscar = tk.Button(self, text="Buscar", command=self.buscar_producto)
        self.boton_buscar.pack(pady=10)

        #entry para buscar
        self.entry_buscar = tk.Entry(self)
        self.entry_buscar.pack(pady=10)

        #obtener datos de la base de datos
        self.obtener_datos()
    def obtener_datos(self):
        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            print("Error al conectar a la base de datos")
            return
        
        cursor.execute("SELECT id_producto, nombre, marca, cantidad, precio FROM producto")
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert("", tk.END, values=row)
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

    def modificar_producto(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Por favor seleccione un producto")
            return
        item=self.tree.item(selected_items)
        record = item['values']

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, record[1])
        self.entry_marca.delete(0, tk.END)
        self.entry_marca.insert(0, record[2])
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, record[3])
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, record[4])
        
        self.id_producto = record[0]

    def guardar_datos(self):
        if not self.validar_campos():
            return
        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error al conectar a la base de datos")
            return
        nombre = self.entry_nombre.get()
        marca = self.entry_marca.get()
        cantidad = int(self.entry_cantidad.get())
        precio = float(self.entry_precio.get())
        query = "UPDATE producto SET nombre=%s, marca=%s, cantidad=%s, precio=%s WHERE id_producto=%s"
        valores = (nombre, marca, cantidad, precio, self.id_producto)
        try:
            cursor.execute(query, valores)
            mydb.commit()
            messagebox.showinfo("Producto Modificado", "El producto ha sido modificado exitosamente")
            self.limpiar_campos()
            self.tree.delete(*self.tree.get_children())
            self.obtener_datos()
        except mysql.connector.Error as e:
            messagebox.showerror("Error al modificar el producto", f"Error: {e}")
        finally:
            cursor.close()
            mydb.close()    

if __name__ == "__main__":
    app = ListadoProductos()
    app.mainloop()