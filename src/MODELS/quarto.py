# MODELS/quarto.py

from DB_CONNECTIONS.mongodb_connection import MongoDBConnection
from DB_CONNECTIONS.mysql_connection import MySQLConnection
from pymongo.errors import DuplicateKeyError, PyMongoError
from mysql.connector import Error as MySQLError
import datetime

class Quarto:
    def __init__(self, num_quarto=None, tipo_quarto=None, valor_diaria=None, 
                 limite_pessoas=None, cpf=None, db_type='mongodb'):
        self.num_quarto = num_quarto
        self.tipo_quarto = tipo_quarto
        self.valor_diaria = valor_diaria
        self.limite_pessoas = limite_pessoas
        self.cpf = cpf
        self.db_type = db_type
        
    def create_quarto(self, db_type='mongodb'):

        if db_type == 'mongodb':
            self._create_quarto_mongodb()
        elif db_type == 'mysql':
            self._create_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _create_quarto_mongodb(self):
        mongo_conn = MongoDBConnection()
        database = mongo_conn.get_db()
        if database is None:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            quarto_collection = database['quarto']
            # Criar índice único no campo 'num_quarto' (executar apenas uma vez)
            quarto_collection.create_index("num_quarto", unique=True)
            
            quarto_data = {
                'num_quarto': self.num_quarto,
                'tipo_quarto': self.tipo_quarto,
                'valor_diaria': self.valor_diaria,
                'limite_pessoas': self.limite_pessoas,
                'cpf': self.cpf
            }
            quarto_collection.insert_one(quarto_data)
            print("Quarto criado com sucesso no MongoDB!")
        except DuplicateKeyError:
            print("Erro: Já existe um quarto com este número no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao inserir no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _create_quarto_mysql(self):
        mysql_conn = MySQLConnection()
        connection = mysql_conn.get_connection()
        if connection is None:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO QUARTO (NUM_QUARTO, TIPO_QUARTO, VALOR_DIARIA, LIMITE_PESSOAS, CPF) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.num_quarto, self.tipo_quarto, self.valor_diaria, self.limite_pessoas, self.cpf)
            )
            connection.commit()
            print("Quarto criado com sucesso no MySQL!")
        except MySQLError as e:
            if e.errno == 1062:  # Entrada duplicada
                print("Erro: Já existe um quarto com este número no MySQL.")
            else:
                print(f"Erro ao inserir no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def update_quarto(self, db_type='mongodb', tipo_quarto=None, valor_diaria=None, limite_pessoas=None, cpf=None):
        if db_type == 'mongodb':
            self._update_quarto_mongodb(tipo_quarto, valor_diaria, limite_pessoas, cpf)
        elif db_type == 'mysql':
            self._update_quarto_mysql(tipo_quarto, valor_diaria, limite_pessoas, cpf)
        else:
            print("Tipo de banco de dados inválido.")

    def _update_quarto_mongodb(self, tipo_quarto, valor_diaria, limite_pessoas, cpf):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return
            quarto_collection = database['quarto']
            update_fields = {}
            if tipo_quarto:
                update_fields['tipo_quarto'] = tipo_quarto
            if valor_diaria:
                update_fields['valor_diaria'] = valor_diaria
            if limite_pessoas:
                update_fields['limite_pessoas'] = limite_pessoas
            if cpf is not None:
                update_fields['cpf'] = cpf  # Pode ser None para liberar o quarto

            if update_fields:
                result = quarto_collection.update_one(
                    {'num_quarto': self.num_quarto},
                    {'$set': update_fields}
                )
                if result.matched_count:
                    print("Quarto atualizado com sucesso no MongoDB!")
                else:
                    print("Quarto não encontrado no MongoDB.")
            else:
                print("Nenhum campo para atualizar.")
        except PyMongoError as e:
            print(f"Erro ao atualizar no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _update_quarto_mysql(self, tipo_quarto, valor_diaria, limite_pessoas, cpf):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Erro na conexão com o MySQL.")
                return
            cursor = connection.cursor()
            update_fields = []
            update_values = []

            if tipo_quarto:
                update_fields.append("TIPO_QUARTO = %s")
                update_values.append(tipo_quarto)
            if valor_diaria:
                update_fields.append("VALOR_DIARIA = %s")
                update_values.append(valor_diaria)
            if limite_pessoas:
                update_fields.append("LIMITE_PESSOAS = %s")
                update_values.append(limite_pessoas)
            if cpf is not None:
                update_fields.append("CPF = %s")
                update_values.append(cpf)

            if update_fields:
                update_values.append(self.num_quarto)
                sql = f"UPDATE QUARTO SET {', '.join(update_fields)} WHERE NUM_QUARTO = %s"
                cursor.execute(sql, tuple(update_values))
                connection.commit()
                if cursor.rowcount:
                    print("Quarto atualizado com sucesso no MySQL!")
                else:
                    print("Quarto não encontrado no MySQL.")
            else:
                print("Nenhum campo para atualizar.")
        except MySQLError as e:
            print(f"Erro ao atualizar no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def delete_quarto(self, db_type='mongodb'):
        if db_type == 'mongodb':
            self._delete_quarto_mongodb()
        elif db_type == 'mysql':
            self._delete_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _delete_quarto_mongodb(self):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return
            quarto_collection = database['quarto']
            result = quarto_collection.delete_one({'num_quarto': self.num_quarto})
            if result.deleted_count:
                print("Quarto deletado com sucesso no MongoDB!")
            else:
                print("Quarto não encontrado no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao deletar no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def quarto_exists(num_quarto, db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._quarto_exists_mongodb(num_quarto)
        elif db_type == 'mysql':
            return Quarto._quarto_exists_mysql(num_quarto)
        else:
            print("Tipo de banco de dados inválido.")
            return False

    @staticmethod
    def _quarto_exists_mongodb(num_quarto):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return False

            quarto_collection = database['quarto']
            exists = quarto_collection.count_documents({'num_quarto': num_quarto}) > 0
            return exists
        except PyMongoError as e:
            print(f"Erro ao verificar no MongoDB: {e}")
            return False
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _quarto_exists_mysql(num_quarto):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Erro na conexão com o MySQL.")
                return False

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT NUM_QUARTO FROM QUARTO WHERE NUM_QUARTO = %s", (num_quarto,))
            resultado = cursor.fetchone()
            return resultado is not None
        except MySQLError as e:
            print(f"Erro ao verificar no MySQL: {e}")
            return False
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def get_quarto(num_quarto, db_type='mongodb'):
        """
        Busca as informações do quarto no banco de dados selecionado.
        """
        try:
            if db_type == 'mongodb':
                db = MongoDBConnection()
                if not db.get_db():
                    return None
                quarto_collection = db.get_db()['quarto']
                quarto = quarto_collection.find_one({'num_quarto': num_quarto})
                db.close_connection()
                return quarto

            elif db_type == 'mysql':
                mysql_conn = MySQLConnection()
                if not mysql_conn.get_connection():
                    return None
                connection = mysql_conn.get_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM QUARTO WHERE NUM_QUARTO = %s", (num_quarto,))
                result = cursor.fetchone()
                cursor.close()
                mysql_conn.close_connection()

                if result:
                    # Suponha que o resultado tenha todos os campos necessários para o quarto
                    return {
                        'num_quarto': result[0],
                        'valor_diaria': result[1],  # Exemplo de campo
                        'descricao': result[2],      # Exemplo de campo
                        # adicione outros campos conforme necessário
                    }

            else:
                print("Tipo de banco de dados inválido.")
                return None
        except Exception as e:
            print(f"Erro ao obter quarto: {e}")
            return None
        
    @staticmethod
    def get_total_quarto(db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._get_total_quarto_mongodb()
        elif db_type == 'mysql':
            return Quarto._get_total_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_quarto_mongodb():
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                return 0
            quarto_collection = database['quarto']
            total = quarto_collection.count_documents({})
            return total
        except PyMongoError as e:
            print(f"Erro ao obter total de quarto no MongoDB: {e}")
            return 0
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_total_quarto_mysql():
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                return 0
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM QUARTO")
            total = cursor.fetchone()[0]
            return total
        except MySQLError as e:
            print(f"Erro ao obter total de quarto no MySQL: {e}")
            return 0
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def atualizar_cpf(self, db_type='mongodb'):
        if db_type == 'mongodb':
            self._atualizar_cpf_mongodb()
        elif db_type == 'mysql':
            self._atualizar_cpf_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _atualizar_cpf_mongodb(self):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return
            quarto_collection = database['quarto']
            result = quarto_collection.update_one(
                {'num_quarto': self.num_quarto},
                {'$set': {'cpf': self.cpf}}
            )
            if result.matched_count:
                print("CPF do hóspede atualizado com sucesso no MongoDB!")
            else:
                print("Quarto não encontrado no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao atualizar CPF no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _atualizar_cpf_mysql(self):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Erro na conexão com o MySQL.")
                return
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE QUARTO SET CPF = %s WHERE NUM_QUARTO = %s",
                (self.cpf, self.num_quarto)
            )
            connection.commit()
            if cursor.rowcount:
                print("CPF do hóspede atualizado com sucesso no MySQL!")
            else:
                print("Quarto não encontrado no MySQL.")
        except MySQLError as e:
            print(f"Erro ao atualizar CPF no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def quarto_exists(num_quarto, db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._quarto_exists_mongodb(num_quarto)
        elif db_type == 'mysql':
            return Quarto._quarto_exists_mysql(num_quarto)
        else:
            print("Tipo de banco de dados inválido.")
            return False

    @staticmethod
    def _quarto_exists_mongodb(num_quarto):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return False

            quarto_collection = database['quarto']
            exists = quarto_collection.count_documents({'num_quarto': num_quarto}) > 0
            return exists
        except PyMongoError as e:
            print(f"Erro ao verificar no MongoDB: {e}")
            return False
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _quarto_exists_mysql(num_quarto):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Erro na conexão com o MySQL.")
                return False

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT NUM_QUARTO FROM QUARTO WHERE NUM_QUARTO = %s", (num_quarto,))
            resultado = cursor.fetchone()
            return resultado is not None
        except MySQLError as e:
            print(f"Erro ao verificar no MySQL: {e}")
            return False
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def get_quarto(num_quarto, db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._get_quarto_mongodb(num_quarto)
        elif db_type == 'mysql':
            return Quarto._get_quarto_mysql(num_quarto)
        else:
            print("Tipo de banco de dados inválido.")
            return None

    @staticmethod
    def _get_quarto_mongodb(num_quarto):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return None

            quarto_collection = database['quarto']
            quarto_data = quarto_collection.find_one({'num_quarto': num_quarto})
            return quarto_data
        except PyMongoError as e:
            print(f"Erro ao buscar quarto no MongoDB: {e}")
            return None
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_quarto_mysql(num_quarto):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Falha na conexão com o MySQL.")
                return None

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM QUARTO WHERE NUM_QUARTO = %s", (num_quarto,))
            quarto = cursor.fetchone()
            return quarto
        except MySQLError as e:
            print(f"Erro ao buscar quarto no MySQL: {e}")
            return None
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def get_total_quarto(db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._get_total_quarto_mongodb()
        elif db_type == 'mysql':
            return Quarto._get_total_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_quarto_mongodb():
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                return 0
            quarto_collection = database['quarto']
            total = quarto_collection.count_documents({})
            return total
        except PyMongoError as e:
            print(f"Erro ao obter total de quarto no MongoDB: {e}")
            return 0
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_total_quarto_mysql():
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                return 0
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM QUARTO")
            total = cursor.fetchone()[0]
            return total
        except MySQLError as e:
            print(f"Erro ao obter total de quarto no MySQL: {e}")
            return 0
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def atualizar_cpf(self, db_type='mongodb'):
        if db_type == 'mongodb':
            self._atualizar_cpf_mongodb()
        elif db_type == 'mysql':
            self._atualizar_cpf_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _atualizar_cpf_mongodb(self):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return
            quarto_collection = database['quarto']
            result = quarto_collection.update_one(
                {'num_quarto': self.num_quarto},
                {'$set': {'cpf': self.cpf}}
            )
            if result.matched_count:
                print("CPF do hóspede atualizado com sucesso no MongoDB!")
            else:
                print("Quarto não encontrado no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao atualizar CPF no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _atualizar_cpf_mysql(self):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Erro na conexão com o MySQL.")
                return
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE QUARTO SET CPF = %s WHERE NUM_QUARTO = %s",
                (self.cpf, self.num_quarto)
            )
            connection.commit()
            if cursor.rowcount:
                print("CPF do hóspede atualizado com sucesso no MySQL!")
            else:
                print("Quarto não encontrado no MySQL.")
        except MySQLError as e:
            print(f"Erro ao atualizar CPF no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def get_quarto(num_quarto, db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._get_quarto_mongodb(num_quarto)
        elif db_type == 'mysql':
            return Quarto._get_quarto_mysql(num_quarto)
        else:
            print("Tipo de banco de dados inválido.")
            return None

    @staticmethod
    def _get_quarto_mongodb(num_quarto):
        try:
            mongo_conn = MongoDBConnection()
            database = mongo_conn.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return None

            quarto_collection = database['quarto']
            quarto_data = quarto_collection.find_one({'num_quarto': num_quarto})
            return quarto_data
        except PyMongoError as e:
            print(f"Erro ao buscar quarto no MongoDB: {e}")
            return None
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_quarto_mysql(num_quarto):
        try:
            mysql_conn = MySQLConnection()
            connection = mysql_conn.get_connection()
            if connection is None:
                print("Falha na conexão com o MySQL.")
                return None

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM QUARTO WHERE NUM_QUARTO = %s", (num_quarto,))
            quarto = cursor.fetchone()
            return quarto
        except MySQLError as e:
            print(f"Erro ao buscar quarto no MySQL: {e}")
            return None
        finally:
            cursor.close()
            mysql_conn.close_connection()
