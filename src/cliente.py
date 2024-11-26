# cliente.py

from mysql_connection import MySQLConnection
from mongodb_connection import MongoDBConnection

class Cliente:
    def __init__(self, cpf, telefone=None, nome=None, email=None, data_nascimento=None, cep=None, db_type='mongodb'):
        self.cpf = cpf
        self.telefone = telefone
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.cep = cep
        self.db_type = db_type

    def create_cliente(self):
        if self.db_type == 'mongodb':
            self._create_cliente_mongodb()
        elif self.db_type == 'mysql':
            self._create_cliente_mysql()
        else:
            print("Tipo de banco de dados inválidoo.")

    def _create_cliente_mongodb(self):
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return
            clientes_collection = db.get_db()['clientes']
            cliente_data = {
                'cpf': self.cpf,
                'telefone': self.telefone,
                'nome': self.nome,
                'email': self.email,
                'data_nascimento': self.data_nascimento,
                'cep': self.cep
            }
            clientes_collection.insert_one(cliente_data)
            print("Cliente criado com sucesso no MongoDB!")
            db.close_connection()
        except Exception as e:
            print(f"Erro ao criar cliente no MongoDB: {e}")

    def _create_cliente_mysql(self):
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO CLIENTE (CPF, TELEFONE, NOME, EMAIL, DATA_NASCIMENTO, CEP) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (self.cpf, self.telefone, self.nome, self.email, self.data_nascimento, self.cep)
            )
            connection.commit()
            print("Cliente criado com sucesso no MySQL!")
            cursor.close()
            db.close_connection()
        except Exception as e:
            print(f"Erro ao criar cliente no MySQL: {e}")

    def update_cliente(self):
        if self.db_type == 'mongodb':
            self._update_cliente_mongodb()
        elif self.db_type == 'mysql':
            self._update_cliente_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _update_cliente_mongodb(self):
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return
            clientes_collection = db.get_db()['clientes']
            update_fields = {}
            if self.telefone is not None:
                update_fields['telefone'] = self.telefone
            if self.nome is not None:
                update_fields['nome'] = self.nome
            if self.email is not None:
                update_fields['email'] = self.email
            if self.data_nascimento is not None:
                update_fields['data_nascimento'] = self.data_nascimento
            if self.cep is not None:
                update_fields['cep'] = self.cep

            if update_fields:
                clientes_collection.update_one(
                    {'cpf': self.cpf},
                    {'$set': update_fields}
                )
                print("Cliente atualizado com sucesso no MongoDB!")
            else:
                print("Nenhum campo para atualizar.")
            db.close_connection()
        except Exception as e:
            print(f"Erro ao atualizar cliente no MongoDB: {e}")

    def _update_cliente_mysql(self):
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return
            connection = db.get_connection()
            cursor = connection.cursor()
            update_fields = []
            update_values = []

            if self.telefone is not None:
                update_fields.append("TELEFONE = %s")
                update_values.append(self.telefone)
            if self.nome is not None:
                update_fields.append("NOME = %s")
                update_values.append(self.nome)
            if self.email is not None:
                update_fields.append("EMAIL = %s")
                update_values.append(self.email)
            if self.data_nascimento is not None:
                update_fields.append("DATA_NASCIMENTO = %s")
                update_values.append(self.data_nascimento)
            if self.cep is not None:
                update_fields.append("CEP = %s")
                update_values.append(self.cep)

            if update_fields:
                update_values.append(self.cpf)
                sql = f"UPDATE CLIENTE SET {', '.join(update_fields)} WHERE CPF = %s"
                cursor.execute(sql, tuple(update_values))
                connection.commit()
                print("Cliente atualizado com sucesso no MySQL!")
            else:
                print("Nenhum campo para atualizar.")
            cursor.close()
            db.close_connection()
        except Exception as e:
            print(f"Erro ao atualizar cliente no MySQL: {e}")

    def delete_cliente(self):
        if self.db_type == 'mongodb':
            self._delete_cliente_mongodb()
        elif self.db_type == 'mysql':
            self._delete_cliente_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _delete_cliente_mongodb(self):
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return
            clientes_collection = db.get_db()['clientes']
            result = clientes_collection.delete_one({'cpf': self.cpf})
            if result.deleted_count > 0:
                print("Cliente deletado com sucesso no MongoDB.")
            else:
                print("Cliente não encontrado no MongoDB.")
            db.close_connection()
        except Exception as e:
            print(f"Erro ao deletar cliente no MongoDB: {e}")

    def _delete_cliente_mysql(self):
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM CLIENTE WHERE CPF = %s", (self.cpf,))
            connection.commit()
            if cursor.rowcount > 0:
                print("Cliente deletado com sucesso no MySQL.")
            else:
                print("Cliente não encontrado no MySQL.")
            cursor.close()
            db.close_connection()
        except Exception as e:
            print(f"Erro ao deletar cliente no MySQL: {e}")

    @staticmethod
    def cliente_exists(cpf, db_type):
        if db_type == 'mongodb':
            return Cliente._cliente_exists_mongodb(cpf)
        elif db_type == 'mysql':
            return Cliente._cliente_exists_mysql(cpf)
        else:
            print("Tipo de banco de dados inválido.")
            return False

    @staticmethod
    def _cliente_exists_mongodb(cpf):
        try:
            db = MongoDBConnection()
            if not db.connected:
                return False
            clientes_collection = db.get_db()['clientes']
            exists = clientes_collection.count_documents({'cpf': cpf}) > 0
            db.close_connection()
            return exists
        except Exception as e:
            print(f"Erro ao verificar cliente no MongoDB: {e}")
            return False

    @staticmethod
    def _cliente_exists_mysql(cpf):
        try:
            db = MySQLConnection()
            if not db.connected:
                return False
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT CPF FROM CLIENTE WHERE CPF = %s", (cpf,))
            result = cursor.fetchone()
            cursor.close()
            db.close_connection()
            return result is not None
        except Exception as e:
            print(f"Erro ao verificar cliente no MySQL: {e}")
            return False

    @staticmethod
    def get_total_clientes(db_type):
        if db_type == 'mongodb':
            return Cliente._get_total_clientes_mongodb()
        elif db_type == 'mysql':
            return Cliente._get_total_clientes_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_clientes_mongodb():
        try:
            db = MongoDBConnection()
            if not db.connected:
                return 0
            clientes_collection = db.get_db()['clientes']
            total = clientes_collection.count_documents({})
            db.close_connection()
            return total
        except Exception as e:
            print(f"Erro ao obter total de clientes no MongoDB: {e}")
            return 0

    @staticmethod
    def _get_total_clientes_mysql():
        try:
            db = MySQLConnection()
            if not db.connected:
                return 0
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM CLIENTE")
            total = cursor.fetchone()[0]
            cursor.close()
            db.close_connection()
            return total
        except Exception as e:
            print(f"Erro ao obter total de clientes no MySQL: {e}")
            return 0
