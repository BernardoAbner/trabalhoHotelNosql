# relatorio.py

import datetime
from mongodb_connection import MongoDBConnection
from mysql_connection import MySQLConnection

class Relatorio:
    @staticmethod
    def visao_de_hotel(db_type):
        if db_type == 'mysql':
            Relatorio._visao_de_hotel_mysql()
        elif db_type == 'mongodb':
            Relatorio._visao_de_hotel_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _visao_de_hotel_mysql():
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()

            # Obter total de quartos
            cursor.execute("SELECT COUNT(*) FROM QUARTO")
            total_quartos = cursor.fetchone()[0]

            # Obter total de quartos ocupados
            cursor.execute("SELECT COUNT(*) FROM QUARTO WHERE CPF IS NOT NULL")
            quartos_ocupados = cursor.fetchone()[0]

            # Obter total de reservas ativas
            cursor.execute("SELECT COUNT(*) FROM RESERVA WHERE DATA_FINAL >= CURDATE()")
            reservas_ativas = cursor.fetchone()[0]

            cursor.close()
            db.close_connection()

            print("\nVisão Geral do Hotel:")
            print("-"*80)
            print(f"Total de Quartos: {total_quartos}")
            print(f"Quartos Ocupados: {quartos_ocupados}")
            print(f"Quartos Disponíveis: {total_quartos - quartos_ocupados}")
            print(f"Reservas Ativas: {reservas_ativas}")
            print("-"*80)

        except Exception as e:
            print(f"Erro ao obter a visão do hotel no MySQL: {e}")

    @staticmethod
    def _visao_de_hotel_mongodb():
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return

            quartos_collection = db.get_db()['quartos']
            reservas_collection = db.get_db()['reservas']

            total_quartos = quartos_collection.count_documents({})
            quartos_ocupados = quartos_collection.count_documents({'cpf': {'$ne': None}})
            reservas_ativas = reservas_collection.count_documents({'data_final': {'$gte': datetime.datetime.now()}})

            db.close_connection()

            print("\nVisão Geral do Hotel:")
            print("-"*80)
            print(f"Total de Quartos: {total_quartos}")
            print(f"Quartos Ocupados: {quartos_ocupados}")
            print(f"Quartos Disponíveis: {total_quartos - quartos_ocupados}")
            print(f"Reservas Ativas: {reservas_ativas}")
            print("-"*80)

        except Exception as e:
            print(f"Erro ao obter a visão do hotel no MongoDB: {e}")

    @staticmethod
    def relatorio_quarto(db_type):
        if db_type == 'mysql':
            Relatorio._relatorio_quarto_mysql()
        elif db_type == 'mongodb':
            Relatorio._relatorio_quarto_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _relatorio_quarto_mysql():
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT NUM_QUARTO, TIPO_QUARTO, VALOR_DIARIA, LIMITE_PESSOAS, CPF
                FROM QUARTO
            """)
            quartos = cursor.fetchall()
            cursor.close()
            db.close_connection()

            if quartos:
                print("\nRelatório de Quartos:")
                print("-"*80)
                for quarto in quartos:
                    num_quarto, tipo_quarto, valor_diaria, limite_pessoas, cpf = quarto
                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Tipo do Quarto: {tipo_quarto}")
                    print(f"Valor da Diária: R${valor_diaria:.2f}")
                    print(f"Limite de Pessoas: {limite_pessoas}")
                    print(f"CPF do Hóspede: {cpf if cpf else 'Disponível'}")
                    print("-"*80)
            else:
                print("Nenhum quarto encontrado.")

        except Exception as e:
            print(f"Erro ao obter os quartos do MySQL: {e}")

    @staticmethod
    def _relatorio_quarto_mongodb():
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return

            collection = db.get_db()['quartos']
            quartos = list(collection.find())

            if quartos:
                print("\nRelatório de Quartos:")
                print("-"*80)
                for quarto in quartos:
                    num_quarto = quarto.get('num_quarto')
                    tipo_quarto = quarto.get('tipo_quarto')
                    valor_diaria = quarto.get('valor_diaria')
                    limite_pessoas = quarto.get('limite_pessoas')
                    cpf = quarto.get('cpf')

                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Tipo do Quarto: {tipo_quarto}")
                    print(f"Valor da Diária: R${valor_diaria:.2f}")
                    print(f"Limite de Pessoas: {limite_pessoas}")
                    print(f"CPF do Hóspede: {cpf if cpf else 'Disponível'}")
                    print("-"*80)
            else:
                print("Nenhum quarto encontrado.")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao obter os quartos do MongoDB: {e}")

    @staticmethod
    def relatorio_clientes(db_type):
        if db_type == 'mysql':
            Relatorio._relatorio_clientes_mysql()
        elif db_type == 'mongodb':
            Relatorio._relatorio_clientes_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _relatorio_clientes_mysql():
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT CPF, NOME, EMAIL, TELEFONE, DATA_NASCIMENTO, CEP
                FROM CLIENTE
            """)
            clientes = cursor.fetchall()
            cursor.close()
            db.close_connection()

            if clientes:
                print("\nLista de Clientes:")
                print("-"*80)
                for cliente in clientes:
                    cpf, nome, email, telefone, data_nascimento, cep = cliente
                    print(f"CPF: {cpf}")
                    print(f"Nome: {nome}")
                    print(f"Email: {email}")
                    print(f"Telefone: {telefone}")
                    print(f"Data de Nascimento: {data_nascimento.strftime('%d-%m-%Y')}")
                    print(f"CEP: {cep}")
                    print("-"*80)
            else:
                print("Nenhum cliente encontrado.")

        except Exception as e:
            print(f"Erro ao obter os clientes do MySQL: {e}")

    @staticmethod
    def _relatorio_clientes_mongodb():
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return

            collection = db.get_db()['clientes']
            clientes = list(collection.find())

            if clientes:
                print("\nLista de Clientes:")
                print("-"*80)
                for cliente in clientes:
                    cpf = cliente.get('cpf')
                    nome = cliente.get('nome')
                    email = cliente.get('email')
                    telefone = cliente.get('telefone')
                    data_nascimento = cliente.get('data_nascimento')
                    cep = cliente.get('cep')

                    # Formatar a data de nascimento se for um objeto datetime
                    if isinstance(data_nascimento, datetime.datetime):
                        data_nascimento = data_nascimento.strftime('%d-%m-%Y')

                    print(f"CPF: {cpf}")
                    print(f"Nome: {nome}")
                    print(f"Email: {email}")
                    print(f"Telefone: {telefone}")
                    print(f"Data de Nascimento: {data_nascimento}")
                    print(f"CEP: {cep}")
                    print("-"*80)
            else:
                print("Nenhum cliente encontrado.")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao obter os clientes do MongoDB: {e}")

    @staticmethod
    def relatorio_reservas(db_type):
        if db_type == 'mysql':
            Relatorio._relatorio_reservas_mysql()
        elif db_type == 'mongodb':
            Relatorio._relatorio_reservas_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _relatorio_reservas_mysql():
        try:
            db = MySQLConnection()
            if not db.connected:
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT NUM_RESERVA, CPF, NUM_QUARTO, DATA_INICIO, DATA_FINAL, VALOR_RESERVA
                FROM RESERVA
            """)
            reservas = cursor.fetchall()
            cursor.close()
            db.close_connection()

            if reservas:
                print("\nLista de Reservas:")
                print("-"*80)
                for reserva in reservas:
                    num_reserva, cpf, num_quarto, data_inicio, data_final, valor_reserva = reserva
                    print(f"Reserva ID: {num_reserva}")
                    print(f"CPF Cliente: {cpf}")
                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Data Início: {data_inicio.strftime('%d-%m-%Y')}")
                    print(f"Data Final: {data_final.strftime('%d-%m-%Y')}")
                    print(f"Valor da Reserva: R${valor_reserva:.2f}")
                    print("-"*80)
            else:
                print("Nenhuma reserva encontrada.")

        except Exception as e:
            print(f"Erro ao obter as reservas do MySQL: {e}")

    @staticmethod
    def _relatorio_reservas_mongodb():
        try:
            db = MongoDBConnection()
            if not db.connected:
                print("Erro na conexão com o MongoDB.")
                return

            collection = db.get_db()['reservas']
            reservas = list(collection.find())

            if reservas:
                print("\nLista de Reservas:")
                print("-"*80)
                for reserva in reservas:
                    num_reserva = reserva.get('num_reserva')
                    cpf_cliente = reserva.get('cpf')
                    num_quarto = reserva.get('num_quarto')
                    data_inicio = reserva.get('data_inicio')
                    data_final = reserva.get('data_final')
                    valor_reserva = reserva.get('valor_reserva')

                    # Formatar as datas se forem objetos datetime
                    if isinstance(data_inicio, datetime.datetime):
                        data_inicio = data_inicio.strftime('%d-%m-%Y')
                    if isinstance(data_final, datetime.datetime):
                        data_final = data_final.strftime('%d-%m-%Y')

                    print(f"Reserva ID: {num_reserva}")
                    print(f"CPF Cliente: {cpf_cliente}")
                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Data Início: {data_inicio}")
                    print(f"Data Final: {data_final}")
                    print(f"Valor da Reserva: R${valor_reserva:.2f}")
                    print("-"*80)
            else:
                print("Nenhuma reserva encontrada.")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao obter as reservas do MongoDB: {e}")
