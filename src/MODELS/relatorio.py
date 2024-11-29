# MODELS/relatorio.py

from DB_CONNECTIONS.mongodb_connection import MongoDBConnection
from DB_CONNECTIONS.mysql_connection import MySQLConnection
import datetime

class Relatorio:
    @staticmethod
    def visao_de_hotel(db_type='mongodb'):
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
            if not db.get_connection():
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()

            # Obter total de quarto
            cursor.execute("SELECT COUNT(*) FROM QUARTO")
            total_quarto = cursor.fetchone()[0]

            # Obter total de quarto ocupados
            cursor.execute("SELECT COUNT(*) FROM QUARTO WHERE CPF IS NOT NULL")
            quarto_ocupados = cursor.fetchone()[0]

            # Obter total de reserva ativas
            cursor.execute("SELECT COUNT(*) FROM RESERVA WHERE DATA_FINAL >= CURDATE()")
            reserva_ativas = cursor.fetchone()[0]

            cursor.close()
            db.close_connection()

            print("\nVisão Geral do Hotel:")
            print("-" * 80)
            print(f"Total de quarto: {total_quarto}")
            print(f"quarto Ocupados: {quarto_ocupados}")
            print(f"quarto Disponíveis: {total_quarto - quarto_ocupados}")
            print(f"reserva Ativas: {reserva_ativas}")
            print("-" * 80)

        except Exception as e:
            print(f"Erro ao obter a visão do hotel no MySQL: {e}")

    @staticmethod
    def _visao_de_hotel_mongodb():
        try:
            db = MongoDBConnection()
            database = db.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return

            quarto_collection = database['quarto']
            reserva_collection = database['reserva']

            total_quarto = quarto_collection.count_documents({})
            quarto_ocupados = quarto_collection.count_documents({'cpf': {'$ne': None}})
            reserva_ativas = reserva_collection.count_documents({'data_final': {'$gte': datetime.datetime.now()}})

            db.close_connection()

            print("\nVisão Geral do Hotel:")
            print("-" * 80)
            print(f"Total de quarto: {total_quarto}")
            print(f"quarto Ocupados: {quarto_ocupados}")
            print(f"quarto Disponíveis: {total_quarto - quarto_ocupados}")
            print(f"reserva Ativas: {reserva_ativas}")
            print("-" * 80)

        except Exception as e:
            print(f"Erro ao obter a visão do hotel no MongoDB: {e}")

    @staticmethod
    def relatorio_quarto(db_type='mongodb'):
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
            if not db.get_connection():
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT NUM_QUARTO, TIPO_QUARTO, VALOR_DIARIA, LIMITE_PESSOAS, CPF
                FROM QUARTO
            """)
            quarto = cursor.fetchall()
            cursor.close()
            db.close_connection()

            if quarto:
                print("\nRelatório de quarto:")
                print("-" * 80)
                for quarto in quarto:
                    num_quarto, tipo_quarto, valor_diaria, limite_pessoas, cpf = quarto
                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Tipo do Quarto: {tipo_quarto}")
                    print(f"Valor da Diária: R${valor_diaria:.2f}")
                    print(f"Limite de Pessoas: {limite_pessoas}")
                    print(f"CPF do Hóspede: {cpf if cpf else 'Disponível'}")
                    print("-" * 80)
            else:
                print("Nenhum quarto encontrado.")

        except Exception as e:
            print(f"Erro ao obter os quarto do MySQL: {e}")

    @staticmethod
    def _relatorio_quarto_mongodb():
        try:
            db = MongoDBConnection()
            database = db.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return

            collection = database['quarto']
            quarto = list(collection.find())

            if quarto:
                print("\nRelatório de quarto:")
                print("-" * 80)
                for quarto in quarto:
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
                    print("-" * 80)
            else:
                print("Nenhum quarto encontrado.")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao obter os quarto do MongoDB: {e}")

    @staticmethod
    def relatorio_cliente(db_type='mongodb'):
        if db_type == 'mysql':
            Relatorio._relatorio_cliente_mysql()
        elif db_type == 'mongodb':
            Relatorio._relatorio_cliente_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _relatorio_cliente_mysql():
        try:
            db = MySQLConnection()
            if not db.get_connection():
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT CPF, NOME, EMAIL, TELEFONE, DATA_NASCIMENTO, CEP
                FROM CLIENTE
            """)
            cliente = cursor.fetchall()
            cursor.close()
            db.close_connection()

            if cliente:
                print("\nLista de cliente:")
                print("-" * 80)
                for cliente in cliente:
                    cpf, nome, email, telefone, data_nascimento, cep = cliente
                    print(f"CPF: {cpf}")
                    print(f"Nome: {nome}")
                    print(f"Email: {email}")
                    print(f"Telefone: {telefone}")
                    print(f"Data de Nascimento: {data_nascimento.strftime('%d-%m-%Y')}")
                    print(f"CEP: {cep}")
                    print("-" * 80)
            else:
                print("Nenhum cliente encontrado.1")

        except Exception as e:
            print(f"Erro ao obter os cliente do MySQL: {e}")

    @staticmethod
    def _relatorio_cliente_mongodb():
        try:
            db = MongoDBConnection()
            database = db.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return

            collection = database['cliente']
            cliente = list(collection.find())

            if cliente:
                print("\nLista de cliente:")
                print("-" * 80)
                for cliente in cliente:
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
                    print("-" * 80)
            else:
                print("Nenhum cliente encontrado.2")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao obter os cliente do MongoDB: {e}")

    @staticmethod
    def relatorio_reserva(db_type='mongodb'):
        if db_type == 'mysql':
            Relatorio._relatorio_reserva_mysql()
        elif db_type == 'mongodb':
            Relatorio._relatorio_reserva_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _relatorio_reserva_mysql():
        try:
            db = MySQLConnection()
            if not db.get_connection():
                print("Erro na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT NUM_RESERVA, CPF, NUM_QUARTO, DATA_INICIO, DATA_FINAL, VALOR_RESERVA, CAFE_INCLUSO
                FROM RESERVA
            """)
            reserva = cursor.fetchall()
            cursor.close()
            db.close_connection()

            if reserva:
                print("\nLista de reserva:")
                print("-" * 80)
                for reserva in reserva:
                    num_reserva, cpf, num_quarto, data_inicio, data_final, valor_reserva, cafe_incluso = reserva
                    print(f"Reserva ID: {num_reserva}")
                    print(f"CPF Cliente: {cpf}")
                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Data Início: {data_inicio.strftime('%d-%m-%Y')}")
                    print(f"Data Final: {data_final.strftime('%d-%m-%Y')}")
                    print(f"Valor da Reserva: R${valor_reserva:.2f}")
                    print(f"Café Incluso: {'Sim' if cafe_incluso else 'Não'}")
                    print("-" * 80)
            else:
                print("Nenhuma reserva encontrada.")

        except Exception as e:
            print(f"Erro ao obter as reserva do MySQL: {e}")

    @staticmethod
    def _relatorio_reserva_mongodb():
        try:
            db = MongoDBConnection()
            database = db.get_db()
            if database is None:
                print("Erro na conexão com o MongoDB.")
                return

            collection = database['reserva']
            reserva = list(collection.find())

            if reserva:
                print("\nLista de reserva:")
                print("-" * 80)
                for reserva in reserva:
                    num_reserva = reserva.get('num_reserva')
                    cpf_cliente = reserva.get('cpf')
                    num_quarto = reserva.get('num_quarto')
                    data_inicio = reserva.get('data_inicio')
                    data_final = reserva.get('data_final')
                    valor_reserva = reserva.get('valor_reserva')
                    cafe_incluso = reserva.get('cafe_incluso')

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
                    print(f"Café Incluso: {'Sim' if cafe_incluso else 'Não'}")
                    print("-" * 80)
            else:
                print("Nenhuma reserva encontrada.")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao obter as reserva do MongoDB: {e}")

    @staticmethod
    def listar_todos_cliente(db_type='mongodb'):
        if db_type == 'mysql':
            Relatorio._listar_todos_cliente_mysql()
        elif db_type == 'mongodb':
            Relatorio._listar_todos_cliente_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _listar_todos_cliente_mysql():
        try:
            db = MySQLConnection()
            if not db.get_connection():
                print("Falha na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT CPF, NOME, EMAIL, TELEFONE, DATA_NASCIMENTO, CEP
                FROM CLIENTE
            """)
            cliente = cursor.fetchall()

            if cliente:
                print("\nLista de cliente (MySQL):")
                print("-" * 80)
                for cliente in cliente:
                    cpf, nome, email, telefone, data_nascimento, cep = cliente
                    print(f"CPF: {cpf}")
                    print(f"Nome: {nome}")
                    print(f"Email: {email}")
                    print(f"Telefone: {telefone}")
                    print(f"Data de Nascimento: {data_nascimento.strftime('%d-%m-%Y')}")
                    print(f"CEP: {cep}")
                    print("-" * 80)
            else:
                print("Nenhum cliente encontrado.3")

            cursor.close()
            db.close_connection()

        except Exception as e:
            print(f"Erro ao listar cliente no MySQL: {e}")

    @staticmethod
    def _listar_todos_cliente_mongodb():
        try:
            db = MongoDBConnection()
            database = db.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return

            collection = database['cliente']
            cliente = list(collection.find())

            if cliente:
                print("\nLista de cliente (MongoDB):")
                print("-" * 80)
                for cliente in cliente:
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
                    print("-" * 80)
            else:
                print("Nenhum cliente encontrado.4")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao listar cliente no MongoDB: {e}")

    @staticmethod
    def listar_todas_reserva(db_type='mongodb'):
        if db_type == 'mysql':
            Relatorio._listar_todas_reserva_mysql()
        elif db_type == 'mongodb':
            Relatorio._listar_todas_reserva_mongodb()
        else:
            print("Tipo de banco de dados inválido.")

    @staticmethod
    def _listar_todas_reserva_mysql():
        try:
            db = MySQLConnection()
            if not db.get_connection():
                print("Falha na conexão com o MySQL.")
                return

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT NUM_RESERVA, CPF, NUM_QUARTO, DATA_INICIO, DATA_FINAL, VALOR_RESERVA, CAFE_INCLUSO
                FROM RESERVA
            """)
            reserva = cursor.fetchall()

            if reserva:
                print("\nLista de reserva (MySQL):")
                print("-" * 80)
                for reserva in reserva:
                    num_reserva, cpf, num_quarto, data_inicio, data_final, valor_reserva, cafe_incluso = reserva
                    print(f"Reserva ID: {num_reserva}")
                    print(f"CPF Cliente: {cpf}")
                    print(f"Número do Quarto: {num_quarto}")
                    print(f"Data Início: {data_inicio.strftime('%d-%m-%Y')}")
                    print(f"Data Final: {data_final.strftime('%d-%m-%Y')}")
                    print(f"Valor da Reserva: R${valor_reserva:.2f}")
                    print(f"Café Incluso: {'Sim' if cafe_incluso else 'Não'}")
                    print("-" * 80)
            else:
                print("Nenhuma reserva encontrada.")

            cursor.close()
            db.close_connection()

        except Exception as e:
            print(f"Erro ao listar reserva no MySQL: {e}")

    @staticmethod
    def _listar_todas_reserva_mongodb():
        try:
            db = MongoDBConnection()
            database = db.get_db()
            if database is None:
                print("Falha na conexão com o MongoDB.")
                return

            collection = database['reserva']
            reserva = list(collection.find())

            if reserva:
                print("\nLista de reserva (MongoDB):")
                print("-" * 80)
                for reserva in reserva:
                    num_reserva = reserva.get('num_reserva')
                    cpf_cliente = reserva.get('cpf')
                    num_quarto = reserva.get('num_quarto')
                    data_inicio = reserva.get('data_inicio')
                    data_final = reserva.get('data_final')
                    valor_reserva = reserva.get('valor_reserva')
                    cafe_incluso = reserva.get('cafe_incluso')

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
                    print(f"Café Incluso: {'Sim' if cafe_incluso else 'Não'}")
                    print("-" * 80)
            else:
                print("Nenhuma reserva encontrada.")

            db.close_connection()

        except Exception as e:
            print(f"Erro ao listar reserva no MongoDB: {e}")
