# quarto.py

from pymongo.errors import DuplicateKeyError, PyMongoError
from mysql.connector import Error as MySQLError
from mongodb_connection import MongoDBConnection
from mysql_connection import MySQLConnection

class Quarto:
    def __init__(self, num_quarto=None, tipo_quarto=None, valor_diaria=None, 
                 limite_pessoas=None, cpf=None, db_type='mongodb'):
        self.num_quarto = num_quarto
        self.tipo_quarto = tipo_quarto
        self.valor_diaria = valor_diaria
        self.limite_pessoas = limite_pessoas
        self.cpf = cpf
        self.db_type = db_type

    def create_quarto(self):
        if self.db_type == 'mongodb':
            self._create_quarto_mongodb()
        elif self.db_type == 'mysql':
            self._create_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _create_quarto_mongodb(self):
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            db = mongo_conn.get_db()
            quartos_collection = db['quartos']
            quarto_data = {
                'num_quarto': self.num_quarto,
                'tipo_quarto': self.tipo_quarto,
                'valor_diaria': self.valor_diaria,
                'limite_pessoas': self.limite_pessoas,
                'cpf': self.cpf
            }
            quartos_collection.insert_one(quarto_data)
            print("Quarto criado com sucesso no MongoDB!")
        except DuplicateKeyError:
            print("Erro: Já existe um quarto com este número no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao inserir no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _create_quarto_mysql(self):
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO QUARTO (NUM_QUARTO, TIPO_QUARTO, VALOR_DIARIA, LIMITE_PESSOAS, CPF) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.num_quarto, self.tipo_quarto, self.valor_diaria, 
                 self.limite_pessoas, self.cpf)
            )
            db.commit()
            print("Quarto criado com sucesso no MySQL!")
        except MySQLError as e:
            if e.errno == 1062:  # Código de erro para entrada duplicada
                print("Erro: Já existe um quarto com este número no MySQL.")
            else:
                print(f"Erro ao inserir no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def atualizar_cpf(self):
        if self.db_type == 'mongodb':
            self._atualizar_cpf_mongodb()
        elif self.db_type == 'mysql':
            self._atualizar_cpf_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _atualizar_cpf_mongodb(self):
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            db = mongo_conn.get_db()
            quartos_collection = db['quartos']
            quartos_collection.update_one(
                {'num_quarto': self.num_quarto},
                {'$set': {'cpf': self.cpf}}
            )
            print("CPF atualizado com sucesso no MongoDB!")
        except PyMongoError as e:
            print(f"Erro ao atualizar CPF no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _atualizar_cpf_mysql(self):
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE QUARTO SET CPF = %s WHERE NUM_QUARTO = %s",
                (self.cpf, self.num_quarto)
            )
            db.commit()
            print("CPF atualizado com sucesso no MySQL!")
        except MySQLError as e:
            print(f"Erro ao atualizar CPF no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def delete_quarto(self):
        if self.db_type == 'mongodb':
            self._delete_quarto_mongodb()
        elif self.db_type == 'mysql':
            self._delete_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _delete_quarto_mongodb(self):
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            db = mongo_conn.get_db()
            quartos_collection = db['quartos']
            quartos_collection.delete_one({'num_quarto': self.num_quarto})
            print("Quarto deletado com sucesso no MongoDB!")
        except PyMongoError as e:
            print(f"Erro ao deletar quarto no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _delete_quarto_mysql(self):
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            cursor.execute("DELETE FROM QUARTO WHERE NUM_QUARTO = %s", (self.num_quarto,))
            db.commit()
            print("Quarto deletado com sucesso no MySQL!")
        except MySQLError as e:
            print(f"Erro ao deletar quarto no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def update_quarto(self):
        if self.db_type == 'mongodb':
            self._update_quarto_mongodb()
        elif self.db_type == 'mysql':
            self._update_quarto_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _update_quarto_mongodb(self):
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            db = mongo_conn.get_db()
            quartos_collection = db['quartos']
            update_fields = {}
            if self.tipo_quarto:
                update_fields['tipo_quarto'] = self.tipo_quarto
            if self.valor_diaria:
                update_fields['valor_diaria'] = self.valor_diaria
            if self.limite_pessoas:
                update_fields['limite_pessoas'] = self.limite_pessoas
            if self.cpf:
                update_fields['cpf'] = self.cpf

            if update_fields:
                quartos_collection.update_one(
                    {'num_quarto': self.num_quarto},
                    {'$set': update_fields}
                )
                print("Quarto atualizado com sucesso no MongoDB!")
            else:
                print("Nenhum campo para atualizar.")
        except PyMongoError as e:
            print(f"Erro ao atualizar quarto no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _update_quarto_mysql(self):
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            update_fields = []
            update_values = []

            if self.tipo_quarto:
                update_fields.append("TIPO_QUARTO = %s")
                update_values.append(self.tipo_quarto)
            if self.valor_diaria:
                update_fields.append("VALOR_DIARIA = %s")
                update_values.append(self.valor_diaria)
            if self.limite_pessoas:
                update_fields.append("LIMITE_PESSOAS = %s")
                update_values.append(self.limite_pessoas)
            if self.cpf:
                update_fields.append("CPF = %s")
                update_values.append(self.cpf)

            if update_fields:
                update_values.append(self.num_quarto)
                sql = f"UPDATE QUARTO SET {', '.join(update_fields)} WHERE NUM_QUARTO = %s"
                cursor.execute(sql, tuple(update_values))
                db.commit()
                print("Quarto atualizado com sucesso no MySQL!")
            else:
                print("Nenhum campo para atualizar.")
        except MySQLError as e:
            print(f"Erro ao atualizar quarto no MySQL: {e}")
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
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return False
        try:
            db = mongo_conn.get_db()
            quartos_collection = db['quartos']
            exists = quartos_collection.count_documents({'num_quarto': num_quarto}) > 0
            return exists
        except PyMongoError as e:
            print(f"Erro ao verificar no MongoDB: {e}")
            return False
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _quarto_exists_mysql(num_quarto):
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            print("Operação no MySQL não pôde ser realizada.")
            return False
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            cursor.execute("SELECT NUM_QUARTO FROM QUARTO WHERE NUM_QUARTO=%s", (num_quarto,))
            result = cursor.fetchone()
            return result is not None
        except MySQLError as e:
            print(f"Erro ao verificar no MySQL: {e}")
            return False
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def get_total_quartos(db_type='mongodb'):
        if db_type == 'mongodb':
            return Quarto._get_total_quartos_mongodb()
        elif db_type == 'mysql':
            return Quarto._get_total_quartos_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_quartos_mongodb():
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            return 0
        try:
            db = mongo_conn.get_db()
            collection = db['quartos']
            return collection.count_documents({})
        except Exception as e:
            print(f"Erro ao obter contagem no MongoDB: {e}")
            return 0
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_total_quartos_mysql():
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            return 0
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM QUARTO")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Erro ao obter contagem no MySQL: {e}")
            return 0
        finally:
            cursor.close()
            mysql_conn.close_connection()
