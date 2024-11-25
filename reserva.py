# reserva.py

from pymongo.errors import DuplicateKeyError, PyMongoError
from mysql.connector import Error as MySQLError
from mongodb_connection import MongoDBConnection
from mysql_connection import MySQLConnection
import datetime

class Reserva:
    def __init__(self, num_reserva, data_inicio=None, data_final=None, quantidade_pessoas=None,
                 valor_reserva=None, cpf=None, num_quarto=None, cafe_incluso=None, db_type='mongodb'):
        self.num_reserva = num_reserva
        self.data_inicio = data_inicio
        self.data_final = data_final
        self.quantidade_pessoas = quantidade_pessoas
        self.valor_reserva = valor_reserva
        self.cpf = cpf
        self.num_quarto = num_quarto
        self.cafe_incluso = cafe_incluso
        self.db_type = db_type

    def create_reserva(self):
        if self.db_type == 'mongodb':
            self._create_reserva_mongodb()
        elif self.db_type == 'mysql':
            self._create_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _create_reserva_mongodb(self):
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return
        try:
            db = mongo_conn.get_db()
            reservas_collection = db['reservas']
            reserva_data = {
                'num_reserva': self.num_reserva,
                'data_inicio': self.data_inicio,
                'data_final': self.data_final,
                'quantidade_pessoas': self.quantidade_pessoas,
                'valor_reserva': self.valor_reserva,
                'cpf': self.cpf,
                'num_quarto': self.num_quarto,
                'cafe_incluso': self.cafe_incluso
            }
            reservas_collection.insert_one(reserva_data)
            print("Reserva criada com sucesso no MongoDB!")
        except DuplicateKeyError:
            print("Erro: Já existe uma reserva com este número no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao inserir no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _create_reserva_mysql(self):
        mysql_conn = MySQLConnection()
        if not mysql_conn.connected:
            print("Operação no MySQL não pôde ser realizada.")
            return
        try:
            db = mysql_conn.get_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO RESERVA (NUM_RESERVA, DATA_INICIO, DATA_FINAL, QUANTIDADE_PESSOAS, VALOR_RESERVA, CPF, NUM_QUARTO, CAFE_INCLUSO) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (self.num_reserva, self.data_inicio.strftime('%Y-%m-%d'), self.data_final.strftime('%Y-%m-%d'),
                 self.quantidade_pessoas, self.valor_reserva, self.cpf, self.num_quarto, self.cafe_incluso)
            )
            db.commit()
            print("Reserva criada com sucesso no MySQL!")
        except MySQLError as e:
            if e.errno == 1062:  # Código de erro para entrada duplicada
                print("Erro: Já existe uma reserva com este número no MySQL.")
            else:
                print(f"Erro ao inserir no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def update_reserva(self):
        if self.db_type == 'mongodb':
            self._update_reserva_mongodb()
        elif self.db_type == 'mysql':
            self._update_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _update_reserva_mongodb(self):
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return
            reservas_collection = db.get_db()['reservas']
            update_fields = {}
            if self.data_inicio is not None:
                update_fields['data_inicio'] = self.data_inicio
            if self.data_final is not None:
                update_fields['data_final'] = self.data_final
            if self.quantidade_pessoas is not None:
                update_fields['quantidade_pessoas'] = self.quantidade_pessoas
            if self.valor_reserva is not None:
                update_fields['valor_reserva'] = self.valor_reserva
            if self.cpf is not None:
                update_fields['cpf'] = self.cpf
            if self.num_quarto is not None:
                update_fields['num_quarto'] = self.num_quarto
            if self.cafe_incluso is not None:
                update_fields['cafe_incluso'] = self.cafe_incluso

            if update_fields:
                reservas_collection.update_one(
                    {'num_reserva': self.num_reserva},
                    {'$set': update_fields}
                )
                print("Reserva atualizada com sucesso no MongoDB!")
            else:
                print("Nenhum campo para atualizar.")
            db.close_connection()
        except Exception as e:
            print(f"Erro ao atualizar reserva no MongoDB: {e}")

    def _update_reserva_mysql(self):
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return
            connection = db.get_connection()
            cursor = connection.cursor()
            update_fields = []
            update_values = []

            if self.data_inicio is not None:
                update_fields.append("DATA_INICIO = %s")
                update_values.append(self.data_inicio.strftime('%Y-%m-%d'))
            if self.data_final is not None:
                update_fields.append("DATA_FINAL = %s")
                update_values.append(self.data_final.strftime('%Y-%m-%d'))
            if self.quantidade_pessoas is not None:
                update_fields.append("QUANTIDADE_PESSOAS = %s")
                update_values.append(self.quantidade_pessoas)
            if self.valor_reserva is not None:
                update_fields.append("VALOR_RESERVA = %s")
                update_values.append(self.valor_reserva)
            if self.cpf is not None:
                update_fields.append("CPF = %s")
                update_values.append(self.cpf)
            if self.num_quarto is not None:
                update_fields.append("NUM_QUARTO = %s")
                update_values.append(self.num_quarto)
            if self.cafe_incluso is not None:
                update_fields.append("CAFE_INCLUSO = %s")
                update_values.append(self.cafe_incluso)

            if update_fields:
                update_values.append(self.num_reserva)
                sql = f"UPDATE RESERVA SET {', '.join(update_fields)} WHERE NUM_RESERVA = %s"
                cursor.execute(sql, tuple(update_values))
                connection.commit()
                print("Reserva atualizada com sucesso no MySQL!")
            else:
                print("Nenhum campo para atualizar.")
            cursor.close()
            db.close_connection()
        except Exception as e:
            print(f"Erro ao atualizar reserva no MySQL: {e}")

    def delete_reserva(self):
        if self.db_type == 'mongodb':
            self._delete_reserva_mongodb()
        elif self.db_type == 'mysql':
            self._delete_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _delete_reserva_mongodb(self):
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return
            reservas_collection = db.get_db()['reservas']
            result = reservas_collection.delete_one({'num_reserva': self.num_reserva})
            if result.deleted_count > 0:
                print("Reserva deletada com sucesso no MongoDB.")
            else:
                print("Reserva não encontrada no MongoDB.")
            db.close_connection()
        except Exception as e:
            print(f"Erro ao deletar reserva no MongoDB: {e}")

    def _delete_reserva_mysql(self):
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM RESERVA WHERE NUM_RESERVA = %s", (self.num_reserva,))
            connection.commit()
            if cursor.rowcount > 0:
                print("Reserva deletada com sucesso no MySQL.")
            else:
                print("Reserva não encontrada no MySQL.")
            cursor.close()
            db.close_connection()
        except Exception as e:
            print(f"Erro ao deletar reserva no MySQL: {e}")

    @staticmethod
    def reserva_exists(num_reserva, db_type='mongodb'):
        if db_type == 'mongodb':
            return Reserva._reserva_exists_mongodb(num_reserva)
        elif db_type == 'mysql':
            return Reserva._reserva_exists_mysql(num_reserva)
        else:
            print("Tipo de banco de dados inválido.")
            return False

    @staticmethod
    def _reserva_exists_mongodb(num_reserva):
        mongo_conn = MongoDBConnection()
        if not mongo_conn.connected:
            print("Operação no MongoDB não pôde ser realizada.")
            return False
        try:
            db = mongo_conn.get_db()
            reservas_collection = db['reservas']
            exists = reservas_collection.count_documents({'num_reserva': num_reserva}) > 0
            return exists
        except PyMongoError as e:
            print(f"Erro ao verificar no MongoDB: {e}")
            return False
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _reserva_exists_mysql(num_reserva):
        try:
            db = MySQLConnection()
            if not db.connected:
                return False
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT NUM_RESERVA FROM RESERVA WHERE NUM_RESERVA = %s", (num_reserva,))
            result = cursor.fetchone()
            cursor.close()
            db.close_connection()
            return result is not None
        except Exception as e:
            print(f"Erro ao verificar reserva no MySQL: {e}")
            return False

    @staticmethod
    def get_total_reservas(db_type='mongodb'):
        if db_type == 'mongodb':
            return Reserva._get_total_reservas_mongodb()
        elif db_type == 'mysql':
            return Reserva._get_total_reservas_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_reservas_mongodb():
        try:
            db = MongoDBConnection()
            if not db.connected:
                return 0
            reservas_collection = db.get_db()['reservas']
            total = reservas_collection.count_documents({})
            db.close_connection()
            return total
        except Exception as e:
            print(f"Erro ao obter total de reservas no MongoDB: {e}")
            return 0

    @staticmethod
    def _get_total_reservas_mysql():
        try:
            db = MySQLConnection()
            if not db.connected:
                return 0
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM RESERVA")
            total = cursor.fetchone()[0]
            cursor.close()
            db.close_connection()
            return total
        except Exception as e:
            print(f"Erro ao obter total de reservas no MySQL: {e}")
            return 0
