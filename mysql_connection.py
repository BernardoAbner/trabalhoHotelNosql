import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'trabalho'
        self.user = 'root'
        self.password = '123456'
        self.connection = None
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, 
                database=self.database,  
                user=self.user,  
                password=self.password
            )
            
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("Conectado ao servidor MySQL versão", db_info)
                cursor = self.connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("Conectado ao banco de dados:", record)
                cursor.close()
                self.connected = True

        except Error as e:
            print("Erro ao conectar ao MySQL:", e)
            self.connected = False

    def get_connection(self):
        if self.connected:
            return self.connection
        else:
            print("Conexão não estabelecida com o banco de dados.")
            return None

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão com o MySQL foi encerrada")
