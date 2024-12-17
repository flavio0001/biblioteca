import mysql.connector

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="biblioteca"
    )