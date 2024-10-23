import mysql.connector

def conectar_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",  # PONER SU PROPIO USUARIO
            password="",  # PONER SU PROPIA CLAVE
            database="base_peluquerias"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None