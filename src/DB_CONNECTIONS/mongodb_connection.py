# db_connections/mongodb_connection.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBConnection:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="hoteldb"):
        self.uri = uri
        self.db_name ='hoteldb'
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verificar a conexão usando 'ping'
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print("Conectado ao MongoDB com sucesso.")
        except ConnectionFailure as e:
            print(f"Falha na conexão com o MongoDB: {e}")
            self.db = None
        except Exception as e:
            print(f"Erro inesperado ao conectar ao MongoDB: {e}")
            self.db = None

    def get_db(self):
        return self.db

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Conexão com o MongoDB fechada.")
