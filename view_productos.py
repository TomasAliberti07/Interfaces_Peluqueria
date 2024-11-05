import os
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from conexionbd import conectar_db
from alta_producto import AltaProducto

class ListadoProductos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Listado de Productos")
        self.attributes('-fullscreen', True)

        # Establecer fondo
        self.configure(bg="#40E0D0")

        # Frame para la fila de botones
        self.frame_botones = tk.Frame(self, bg="#40E0D0")
        self.frame_botones.pack(fill=tk.X, pady=10)

        # Botón buscar y campo de entrada
        self.entry_buscar = tk.Entry(self.frame_botones, width=30, font=('calibri', 13))
        self.entry_buscar.pack(side=tk.LEFT, padx=10)
        self.boton_buscar = tk.Button(self.frame_botones, text="BUSCAR", command=self.buscar_producto, width=15, height=2, font=('calibri', 13))
        self.boton_buscar.pack(side=tk.LEFT, padx=10)

        # Botón agregar producto 
        self.boton_agregar = tk.Button(self.frame_botones, text="+ AGREGAR", command=self.abrir_alta_producto, width=15, height=2, font=('calibri', 13))
        self.boton_agregar.pack(side=tk.LEFT, padx=10)

        # Botón modificar
        self.boton_modificar = tk.Button(self.frame_botones, text="MODIFICAR", command=self.modificar_producto, width=15, height=2, font=('calibri', 13))
        self.boton_modificar.pack(side=tk.LEFT, padx=10)

        # Botón eliminar
        self.boton_eliminar = tk.Button(self.frame_botones, text="ELIMINAR", command=self.eliminar_producto, width=15, height=2, font=('calibri', 13))
        self.boton_eliminar.pack(side=tk.LEFT, padx=10)

        # Botón actualizar
        self.boton_actualizar = tk.Button(self.frame_botones, text="ACTUALIZAR", command=self.actualizar_treeview, width=15, height=2, font=('calibri', 13))
        self.boton_actualizar.pack(side=tk.LEFT, padx=10)

        # Botón para volver al menú
        boton_volver = tk.Button(self.frame_botones, text="VOLVER", command=self.volver_menu, width=15, height=2, font=('calibri', 13))
        boton_volver.pack(side=tk.RIGHT, padx=10)

        # Crear Treeview
        self.tree = ttk.Treeview(self, columns=("nombre", "marca", "cantidad", "precio"), show='headings')
        self.tree.heading("nombre", text="NOMBRE")
        self.tree.heading("marca", text="MARCA")
        self.tree.heading("cantidad", text="CANTIDAD")
        self.tree.heading("precio", text="PRECIO")

        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.frame_modificar = tk.Frame(self, bg="#40E0D0")
        self.frame_modificar.pack(pady=10)

        label_nombre = tk.Label(self.frame_modificar, text="NOMBRE:", bg="#40E0D0", font=('calibri', 13))
        label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(self.frame_modificar)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        label_marca = tk.Label(self.frame_modificar, text="MARCA:", bg="#40E0D0", font=('calibri', 13))
        label_marca.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_marca = tk.Entry(self.frame_modificar)
        self.entry_marca.grid(row=1, column=1, padx=5, pady=5)

        label_cantidad = tk.Label(self.frame_modificar, text="CANTIDAD:", bg="#40E0D0", font=('calibri', 13))
        label_cantidad.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_cantidad = tk.Entry(self.frame_modificar)
        
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5)

        label_precio = tk.Label(self.frame_modificar, text="PRECIO :", bg="#40E0D0", font=('calibri', 13))
        label_precio.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_precio = tk.Entry(self.frame_modificar)
        self.entry_precio.grid(row=3, column=1, padx=5, pady=5)

        self.boton_guardar = tk.Button(self.frame_modificar, text="GUARDAR CAMBIOS", command=self.guardar_cambios, width=15, height=2, font=('calibri', 13))
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
            row_upper = (row[1].upper(), row[2].upper(), row[3], row[4]) 
            self.tree.insert("", tk.END, values=row_upper)

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
        self.entry_nombre.insert(0, record[0])  # Nombre
        self.entry_marca.delete(0, tk.END)
        self.entry_marca.insert(0, record[1])  # Marca
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, record[2])  # Cantidad
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, record[3])  # Precio

        # Obtener el id_producto correspondiente
        mydb, cursor = conectar_db()
        cursor.execute("SELECT id_producto FROM producto WHERE nombre=%s AND marca=%s", (record[0], record[1]))
        self.producto_id = cursor.fetchone()[0]  # Guardar el id_producto
        cursor.close()
        mydb.close()

    def guardar_cambios(self):
        if not self.validar_campos():
            return

        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return

        nombre = self.entry_nombre.get().upper()
        marca = self.entry_marca.get().upper()
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
        if not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "El precio debe ser un número")
            return False
        return True

    def buscar_producto(self):
        buscar_texto = self.entry_buscar.get().upper() 
        if not buscar_texto:
            return

        mydb, cursor = conectar_db()
        if mydb is None or cursor is None:
            messagebox.showerror("Error", "Error al conectar a la base de datos")
            return
        query = "SELECT nombre, marca, cantidad, precio FROM producto WHERE nombre LIKE %s OR marca LIKE %s"
        valores = (f"%{buscar_texto}%", f"%{buscar_texto}%")

        try:
            cursor.execute(query, valores)
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                row_upper = (row[0].upper(), row[1].upper(), row[2], row[3])
                self.tree.insert("", tk.END, values=row_upper)
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

    def actualizar_treeview(self):
        self.tree.delete(*self.tree.get_children())  # Limpiar el Treeview
        self.obtener_datos()  # Volver a obtener los datos de la base de datos

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = ListadoProductos(master=root)
    app.mainloop()