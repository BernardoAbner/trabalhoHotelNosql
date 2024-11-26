from pymongo import MongoClient, errors

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.connected = False
        self.connect()

    def connect(self):
        try:
            # Adjust the URI and database name as needed
            self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Force connection to check if the server is available
            self.db = self.client['hoteldb']  # Use your database name
            self.connected = True
        except errors.ServerSelectionTimeoutError as err:
            print("Erro: Não foi possível conectar ao MongoDB.")
            print(err)
            self.connected = False

    def get_db(self):
        if self.connected:
            return self.db
        else:
            print("Conexão não estabelecida com o banco de dados.")
            return None

    def close_connection(self):
        if self.client:
            self.client.close()
