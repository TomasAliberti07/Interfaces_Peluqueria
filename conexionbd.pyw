import mysql.connector

def conectar_bd():
    cnx = mysql.connector.connect(
        user='ramye',
        password='1234567',
        host='localhost',  # Asumiendo que el servidor MySQL está en tu máquina local
        port='3306',       # Especifica el puerto si no es el predeterminado 3306
        database='base_peluquerias'
    )
    return cnx