from DB_CONNECTIONS.mongodb_connection import MongoDBConnection
from DB_CONNECTIONS.mysql_connection import MySQLConnection
from pymongo.errors import DuplicateKeyError, PyMongoError
from mysql.connector import Error as MySQLError
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
        """Cria uma reserva dependendo do tipo de banco de dados especificado."""
        if self.db_type == 'mongodb':
            self._create_reserva_mongodb()
        elif self.db_type == 'mysql':
            self._create_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _create_reserva_mongodb(self):
        """Cria uma reserva no MongoDB."""
        try:
            mongo_conn = MongoDBConnection()
            db = mongo_conn.get_db()
            if db is None:
                print("Operação no MongoDB não pôde ser realizada.")
                return

            reserva_collection = db['reserva']
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
            reserva_collection.insert_one(reserva_data)
            print("Reserva criada com sucesso no MongoDB!")
        except DuplicateKeyError:
            print("Erro: Já existe uma reserva com este número no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao inserir no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _create_reserva_mysql(self):
        """Cria uma reserva no MySQL."""
        try:
            mysql_conn = MySQLConnection()
            db = mysql_conn.get_connection()
            if db is None:
                print("Operação no MySQL não pôde ser realizada.")
                return

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
        """Atualiza uma reserva dependendo do tipo de banco de dados especificado."""
        if self.db_type == 'mongodb':
            self._update_reserva_mongodb()
        elif self.db_type == 'mysql':
            self._update_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _update_reserva_mongodb(self):
        """Atualiza uma reserva no MongoDB."""
        try:
            mongo_conn = MongoDBConnection()
            db = mongo_conn.get_db()
            if db is None:
                print("Erro na conexão com o MongoDB.")
                return

            reserva_collection = db['reserva']
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
                reserva_collection.update_one(
                    {'num_reserva': self.num_reserva},
                    {'$set': update_fields}
                )
                print("Reserva atualizada com sucesso no MongoDB!")
            else:
                print("Nenhum campo para atualizar.")
        except PyMongoError as e:
            print(f"Erro ao atualizar reserva no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _update_reserva_mysql(self):
        """Atualiza uma reserva no MySQL."""
        try:
            mysql_conn = MySQLConnection()
            db = mysql_conn.get_connection()
            if db is None:
                print("Erro na conexão com o MySQL.")
                return

            cursor = db.cursor()
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
                db.commit()
                print("Reserva atualizada com sucesso no MySQL!")
            else:
                print("Nenhum campo para atualizar.")
        except MySQLError as e:
            print(f"Erro ao atualizar reserva no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    def delete_reserva(self):
        """Deleta uma reserva dependendo do tipo de banco de dados especificado."""
        if self.db_type == 'mongodb':
            self._delete_reserva_mongodb()
        elif self.db_type == 'mysql':
            self._delete_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")

    def _delete_reserva_mongodb(self):
        """Deleta uma reserva no MongoDB."""
        try:
            mongo_conn = MongoDBConnection()
            db = mongo_conn.get_db()
            if db is None:
                print("Erro na conexão com o MongoDB.")
                return

            reserva_collection = db['reserva']
            result = reserva_collection.delete_one({'num_reserva': self.num_reserva})
            if result.deleted_count > 0:
                print("Reserva deletada com sucesso no MongoDB.")
            else:
                print("Reserva não encontrada no MongoDB.")
        except PyMongoError as e:
            print(f"Erro ao deletar reserva no MongoDB: {e}")
        finally:
            mongo_conn.close_connection()

    def _delete_reserva_mysql(self):
        """Deleta uma reserva no MySQL.""" 
        try:
            mysql_conn = MySQLConnection()
            db = mysql_conn.get_connection()
            if db is None:
                print("Erro na conexão com o MySQL.")
                return

            cursor = db.cursor()
            cursor.execute("DELETE FROM RESERVA WHERE NUM_RESERVA = %s", (self.num_reserva,))
            db.commit()
            if cursor.rowcount > 0:
                print("Reserva deletada com sucesso no MySQL.")
            else:
                print("Reserva não encontrada no MySQL.")
        except MySQLError as e:
            print(f"Erro ao deletar reserva no MySQL: {e}")
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def reserva_exists(num_reserva, db_type='mongodb'):
        """Verifica se uma reserva com o número fornecido já existe no banco de dados."""
        if db_type == 'mongodb':
            return Reserva._reserva_exists_mongodb(num_reserva)
        elif db_type == 'mysql':
            return Reserva._reserva_exists_mysql(num_reserva)
        else:
            print("Tipo de banco de dados inválido.")
            return False

    @staticmethod
    def _reserva_exists_mongodb(num_reserva):
        """Verifica se a reserva existe no MongoDB.""" 
        try:
            mongo_conn = MongoDBConnection()
            db = mongo_conn.get_db()
            if db is None:
                print("Erro na conexão com o MongoDB.")
                return False

            reserva_collection = db['reserva']
            reserva = reserva_collection.find_one({'num_reserva': num_reserva})
            return reserva is not None
        except PyMongoError as e:
            print(f"Erro ao verificar reserva no MongoDB: {e}")
            return False
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _reserva_exists_mysql(num_reserva):
        """Verifica se a reserva existe no MySQL.""" 
        try:
            mysql_conn = MySQLConnection()
            db = mysql_conn.get_connection()
            if db is None:
                print("Erro na conexão com o MySQL.")
                return False

            cursor = db.cursor()
            cursor.execute("SELECT 1 FROM RESERVA WHERE NUM_RESERVA = %s", (num_reserva,))
            return cursor.fetchone() is not None
        except MySQLError as e:
            print(f"Erro ao verificar reserva no MySQL: {e}")
            return False
        finally:
            cursor.close()
            mysql_conn.close_connection()

    @staticmethod
    def get_total_reserva(db_type='mongodb'):
        """Retorna o total de reserva no banco de dados especificado."""
        if db_type == 'mongodb':
            return Reserva._get_total_reserva_mongodb()
        elif db_type == 'mysql':
            return Reserva._get_total_reserva_mysql()
        else:
            print("Tipo de banco de dados inválido.")
            return 0

    @staticmethod
    def _get_total_reserva_mongodb():
        """Retorna o total de reserva no MongoDB.""" 
        try:
            mongo_conn = MongoDBConnection()
            db = mongo_conn.get_db()
            if db is None:
                print("Erro na conexão com o MongoDB.")
                return 0

            reserva_collection = db['reserva']
            total_reserva = reserva_collection.count_documents({})
            return total_reserva
        except PyMongoError as e:
            print(f"Erro ao contar as reserva no MongoDB: {e}")
            return 0
        finally:
            mongo_conn.close_connection()

    @staticmethod
    def _get_total_reserva_mysql():
        """Retorna o total de reserva no MySQL.""" 
        try:
            mysql_conn = MySQLConnection()
            db = mysql_conn.get_connection()
            if db is None:
                print("Erro na conexão com o MySQL.")
                return 0

            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM RESERVA")
            total_reserva = cursor.fetchone()[0]
            return total_reserva
        except MySQLError as e:
            print(f"Erro ao contar as reserva no MySQL: {e}")
            return 0
        finally:
            cursor.close()
            mysql_conn.close_connection()
