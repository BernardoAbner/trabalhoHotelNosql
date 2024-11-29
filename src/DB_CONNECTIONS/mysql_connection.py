# db_connections/mysql_connection.py

import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self, host='localhost', user='root', password='', database='trabalho_db'):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '1234'
        self.database = 'trabalho_db'
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conectado ao MySQL com sucesso.")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            self.connection = None

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão com o MySQL fechada.")
