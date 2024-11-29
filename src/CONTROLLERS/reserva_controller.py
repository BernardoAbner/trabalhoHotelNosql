# controllers/reserva_controller.py

from CONTROLLERS.quarto_controller import QuartoController
from DB_CONNECTIONS.mongodb_connection import MongoDBConnection
from DB_CONNECTIONS.mysql_connection import MySQLConnection
from MODELS.reserva import Reserva
from MODELS.cliente import Cliente
from MODELS.quarto import Quarto
import datetime

class ReservaController:
    @staticmethod
    def criar_reserva(num_reserva, cpf, num_quarto, data_inicio_str, data_final_str, quantidade_pessoas, cafe_incluso, db_type='mongodb'):
        """
        Cria uma nova reserva no banco de dados selecionado.
        """
        # Verificar existência do cliente
        if not Cliente.cliente_exists(cpf, db_type):
            print("Cliente não encontrado.")
            return

        # Verificar existência do quarto
        if not Quarto.quarto_exists(num_quarto, db_type):
            print("Quarto não encontrado.")
            return

        try:
            data_inicio = datetime.datetime.strptime(data_inicio_str, "%d-%m-%Y")
            data_final = datetime.datetime.strptime(data_final_str, "%d-%m-%Y")
        except ValueError:
            print("Formato de data inválido. Use DD-MM-YYYY.")
            return

        if data_final <= data_inicio:
            print("A data final deve ser posterior à data de início.")
            return

        # Calcular valor da reserva
        valor_reserva = ReservaController._calcular_valor_reserva(num_quarto, data_inicio, data_final, cafe_incluso, db_type)

        reserva = Reserva(num_reserva, data_inicio, data_final, quantidade_pessoas, valor_reserva, cpf, num_quarto, cafe_incluso, db_type)
        reserva.create_reserva()

        # Atualizar quarto para indicar que está ocupado
        QuartoController.atualizar_quarto(num_quarto, cpf=cpf, db_type=db_type)

    @staticmethod
    def _calcular_valor_reserva(num_quarto, data_inicio, data_final, cafe_incluso, db_type):
        """
        Calcula o valor total da reserva com base na diária do quarto e nos dias reservados.
        """
        quarto = Quarto.get_quarto(num_quarto, db_type)
        if not quarto:
            print("Quarto não encontrado para cálculo.")
            return 0

        # Agora acessamos 'valor_diaria' como chave do dicionário
        valor_diaria = quarto.get('valor_diaria')  # Acessando o valor da diária no dicionário
        
        if valor_diaria is None:
            print("Valor da diária não encontrado.")
            return 0
        
        num_dias = (data_final - data_inicio).days
        valor_total = valor_diaria * num_dias
        if cafe_incluso:
            valor_total += 60  # Valor adicional para café da manhã

        return valor_total

    @staticmethod
    def atualizar_reserva(num_reserva, cpf=None, num_quarto=None, data_inicio_str=None, data_final_str=None, quantidade_pessoas=None, cafe_incluso=None, db_type='mongodb'):
        """
        Atualiza as informações de uma reserva existente.
        """
        if not Reserva.reserva_exists(num_reserva, db_type):
            print("Reserva não encontrada.")
            return

        data_inicio = None
        data_final = None
        if data_inicio_str:
            try:
                data_inicio = datetime.datetime.strptime(data_inicio_str, "%d-%m-%Y")
            except ValueError:
                print("Formato de data inválido para data de início.")
                return
        if data_final_str:
            try:
                data_final = datetime.datetime.strptime(data_final_str, "%d-%m-%Y")
            except ValueError:
                print("Formato de data inválido para data final.")
                return

        if data_inicio and data_final and data_final <= data_inicio:
            print("A data final deve ser posterior à data de início.")
            return

        # Recalcular valor da reserva se necessário
        valor_reserva = None
        if (data_inicio and data_final) and num_quarto:
            valor_reserva = ReservaController._calcular_valor_reserva(num_quarto, data_inicio, data_final, cafe_incluso, db_type)

        reserva = Reserva(num_reserva, data_inicio, data_final, quantidade_pessoas, valor_reserva, cpf, num_quarto, cafe_incluso, db_type)
        reserva.update_reserva()

    @staticmethod
    def deletar_reserva(num_reserva, db_type='mongodb'):
        """
        Remove uma reserva do banco de dados selecionado.
        """
        if not Reserva.reserva_exists(num_reserva, db_type):
            print("Reserva não encontrada.")
            return

        # Deletar a reserva
        reserva = Reserva(num_reserva, db_type=db_type)
        reserva.delete_reserva()

        # Liberar quarto associado
        quarto_num = ReservaController._get_num_quarto_by_reserva(num_reserva, db_type)
        if quarto_num:
            QuartoController.atualizar_quarto(quarto_num, cpf=None, db_type=db_type)
            print(f"Reserva número {num_reserva} deletada e quarto número {quarto_num} liberado.")
        else:
            print(f"Reserva número {num_reserva} deletada com sucesso.")

    @staticmethod
    def _get_num_quarto_by_reserva(num_reserva, db_type='mongodb'):
        """
        Obtém o número do quarto associado a uma reserva.
        """
        try:
            if db_type == 'mongodb':
                db = MongoDBConnection()
                if not db.get_db():
                    return None
                reserva_collection = db.get_db()['reserva']
                reserva = reserva_collection.find_one({'num_reserva': num_reserva})
                db.close_connection()
                if reserva:
                    return reserva.get('num_quarto')
            elif db_type == 'mysql':
                mysql_conn = MySQLConnection()
                if not mysql_conn.get_connection():
                    return None
                connection = mysql_conn.get_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT NUM_QUARTO FROM RESERVA WHERE NUM_RESERVA = %s", (num_reserva,))
                result = cursor.fetchone()
                cursor.close()
                mysql_conn.close_connection()
                if result:
                    return result[0]
            else:
                print("Tipo de banco de dados inválido.")
        except Exception as e:
            print(f"Erro ao obter número do quarto pela reserva: {e}")
        return None

    @staticmethod
    def listar_reserva(db_type='mongodb'):
        """
        Lista todas as reserva cadastradas.
        """
        total = Reserva.get_total_reserva(db_type)
        print(f"Total de reserva: {total}")
        Reserva.listar_todas_reserva(db_type)
