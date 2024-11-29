# MODELS/cliente.py

from DB_CONNECTIONS.mongodb_connection import MongoDBConnection
from DB_CONNECTIONS.mysql_connection import MySQLConnection
from pymongo.errors import DuplicateKeyError, PyMongoError
from mysql.connector import Error as MySQLError
import datetime

class Cliente:
    def __init__(self, cpf, nome, email, telefone, data_nascimento, cep, db_type='mongodb'):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.cep = cep
        self.db_type = db_type

    def create_cliente(self):
        if self.db_type == 'mongodb':
            self._create_cliente_mongodb()
        elif self.db_type == 'mysql':
            self._create_cliente_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _create_cliente_mongodb(self):
        mongo_conn = MongoDBConnection()
        database = mongo_conn.get_db()
        if database is None:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            cliente_collection = database['cliente']
            # Criar índice único no campo 'cpf' (executar apenas uma vez)
            cliente_collection.create_index("cpf", unique=True)
            
            cliente_data = {
                'cpf': self.cpf,
                'nome': self.nome,
                'email': self.email,
                'telefone': self.telefone,
                'data_nascimento': self.data_nascimento,
                'cep': self.cep
            }
            cliente_collection.insert_one(cliente_data)
            print("Cliente criado com sucesso no MongoDB!")
        except DuplicateKeyError:
            print("Erro: Já existe um cliente com este CPF no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao inserir no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _create_cliente_mysql(self):
        mysql_conn = MySQLConnection(user='seu_usuario', password='sua_senha')  # Substitua pelas suas credenciais
        connection = mysql_conn.get_connection()
        if not connection:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO CLIENTE (CPF, NOME, EMAIL, TELEFONE, DATA_NASCIMENTO, CEP) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (self.cpf, self.nome, self.email, self.telefone, self.data_nascimento.strftime('%Y-%m-%d'), self.cep)
            )
            connection.commit()
            print("Cliente criado com sucesso no MySQL!")
        except MySQLError as e:
            if e.errno == 1062:  # Entrada duplicada
                print("Erro: Já existe um cliente com este CPF no MySQL.")
            else:
                print(f"Erro ao inserir no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def update_cliente(self, nome=None, email=None, telefone=None, data_nascimento=None, cep=None):
        if self.db_type == 'mongodb':
            self._update_cliente_mongodb(nome, email, telefone, data_nascimento, cep)
        elif self.db_type == 'mysql':
            self._update_cliente_mysql(nome, email, telefone, data_nascimento, cep)
        else:
            print("Tipo de banco de dados inválido.")

    def _update_cliente_mongodb(self, nome, email, telefone, data_nascimento, cep):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return
            cliente_collection = database['cliente']
            update_fields = {}
            if nome:
                update_fields['nome'] = nome
            if email:
                update_fields['email'] = email
            if telefone:
                update_fields['telefone'] = telefone
            if data_nascimento:
                update_fields['data_nascimento'] = data_nascimento
            if cep:
                update_fields['cep'] = cep

            if update_fields:
                result = cliente_collection.update_one(
                    {'cpf': self.cpf},
                    {'$set': update_fields}
                )
                if result.matched_count:
                    print("Cliente atualizado com sucesso no MongoDB!")
                else:
                    print("Cliente não encontrado no MongoDB.")
            else:
                print("Nenhum campo para atualizar.")
        except PyMongoError as e:
            print(f"Erro ao atualizar no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _update_cliente_mysql(self, nome, email, telefone, data_nascimento, cep):
        try:
            mysql_conn = MySQLConnection(user='seu_usuario', password='sua_senha')  # Substitua pelas suas credenciais
            connection = mysql_conn.get_connection()
            if not connection:
                print("Erro na conexão com o MySQL.")
                return
            cursor = connection.cursor()
            update_fields = []
            update_values = []

            if nome:
                update_fields.append("NOME = %s")
                update_values.append(nome)
            if email:
                update_fields.append("EMAIL = %s")
                update_values.append(email)
            if telefone:
                update_fields.append("TELEFONE = %s")
                update_values.append(telefone)
            if data_nascimento:
                update_fields.append("DATA_NASCIMENTO = %s")
                update_values.append(data_nascimento.strftime('%Y-%m-%d'))
            if cep:
                update_fields.append("CEP = %s")
                update_values.append(cep)

            if update_fields:
                update_values.append(self.cpf)
                sql = f"UPDATE CLIENTE SET {', '.join(update_fields)} WHERE CPF = %s"
                cursor.execute(sql, tuple(update_values))
                connection.commit()
                if cursor.rowcount:
                    print("Cliente atualizado com sucesso no MySQL!")
                else:
                    print("Cliente não encontrado no MySQL.")
            else:
                print("Nenhum campo para atualizar.")
        except MySQLError as e:
            print(f"Erro ao atualizar no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def delete_cliente(self):
        if self.db_type == 'mongodb':
            self._delete_cliente_mongodb()
        elif self.db_type == 'mysql':
            self._delete_cliente_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _delete_cliente_mongodb(self):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return
            cliente_collection = database['cliente']
            result = cliente_collection.delete_one({'cpf': self.cpf})
            if result.deleted_count:
                print("Cliente deletado com sucesso no MongoDB!")
            else:
                print("Cliente não encontrado no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao deletar no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _delete_cliente_mysql(self,):
        try:
            mysql_conn = MySQLConnection(user='seu_usuario', password='sua_senha')  # Substitua pelas suas credenciais
            connection = mysql_conn.get_connection()
            if not connection:
                print("Erro na conexão com o MySQL.")
                return
            cursor = connection.cursor()
            cursor.execute("DELETE FROM CLIENTE WHERE CPF = %s", (self.cpf,))
            connection.commit()
            if cursor.rowcount:
                print("Cliente deletado com sucesso no MySQL!")
            else:
                print("Cliente não encontrado no MySQL.")
        except MySQLError as e:
            print(f"Erro ao deletar no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def cliente_exists(cpf, db_type='mongodb'):
        if db_type == 'mysql':
            return Cliente._cliente_exists_mysql(cpf)
        elif db_type == 'mongodb':
            return Cliente._cliente_exists_mongodb(cpf)
        else:
            print("Tipo de banco de dados inválido.")
            return False

    @staticmethod
    def _cliente_exists_mongodb(cpf):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return False

            cliente_collection = database['cliente']
            cliente = cliente_collection.find_one({'cpf': cpf})
            mongo_conn.close_connection()
            return cliente is not None

        except PyMongoError as e:
            print(f"Erro ao verificar a existência do cliente no MongoDB: {e}")
            return False

    @staticmethod
    def _cliente_exists_mysql(cpf):
        try:
            mysql_conn = MySQLConnection(user='seu_usuario', password='sua_senha')  # Substitua pelas suas credenciais
            connection = mysql_conn.get_connection()
            if not connection:
                print("Erro na conexão com o MySQL.")
                return False

            cursor = connection.cursor()
            cursor.execute("SELECT CPF FROM CLIENTE WHERE CPF = %s", (cpf,))
            resultado = cursor.fetchone()
            cursor.close()
            mysql_conn.close_connection()
            return resultado is not None

        except MySQLError as e:
            print(f"Erro ao verificar a existência do cliente no MySQL: {e}")
            return False

    @staticmethod
    def get_total_cliente(db_type='mongodb'):
        if db_type == 'mongodb':
            return Cliente._get_total_cliente_mongodb()
        elif db_type == 'mysql':
            return Cliente._get_total_cliente_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_cliente_mongodb():
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                return 0
            cliente_collection = database['cliente']
            total = cliente_collection.count_documents({})
            return total
        except PyMongoError as e:
            print(f"Erro ao obter total de cliente no MongoDB: {e}")
            return 0
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_total_cliente_mysql():
        try:
            mysql_conn = MySQLConnection(user='seu_usuario', password='sua_senha')  # Substitua pelas suas credenciais
            connection = mysql_conn.get_connection()
            if not connection:
                return 0
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM CLIENTE")
            total = cursor.fetchone()[0]
            return total
        except MySQLError as e:
            print(f"Erro ao obter total de cliente no MySQL: {e}")
            return 0
        finally:
            cursor.close()
            mysql_conn.close_connection()
