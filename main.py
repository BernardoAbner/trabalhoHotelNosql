# main.py

import datetime
from cliente import Cliente
from quarto import Quarto
from reserva import Reserva
from relatorio import Relatorio
from mongodb_connection import MongoDBConnection
from mysql_connection import MySQLConnection

def escolher_banco_de_dados():
    while True:
        print("\nSelecione o banco de dados:")
        print("1. MongoDB")
        print("2. MySQL")
        escolha = input("Digite sua opção: ")
        if escolha == '1':
            print("Banco de dados selecionado: MongoDB")
            return 'mongodb'
        elif escolha == '2':
            print("Banco de dados selecionado: MySQL")
            return 'mysql'
        else:
            print("Opção inválida. Tente novamente.")

def menu_de_criacao(db_type):
    try:
        total_clientes = Cliente.get_total_clientes(db_type)
        total_quartos = Quarto.get_total_quartos(db_type)
        total_reservas = Reserva.get_total_reservas(db_type)

        system_name = "Sistema de Gerenciamento de Hotel"
        created_by = (
            "Aidhan Freitas, Henrique Volpini, Samuel Lucas           |\n"
            "| Bernardo Abner, Rafael Barcelos, Lucas Xavier"
        )
        professor = "HOWARD ROATTI"
        disciplina = "Banco de Dados"
        semestre = "2024/2"
        coracao = "❤️"

        print("\n" + "="*60)
        print(f"{system_name:^60}")
        print("="*60)
        print("TOTAL DE REGISTROS:")
        print("-"*60)
        print(f"| Número de Clientes:                               {str(total_clientes).rjust(5)} |")
        print("-"*60)
        print(f"| Número de Quartos:                                {str(total_quartos).rjust(5)} |")
        print("-"*60)
        print(f"| Número de Reservas:                               {str(total_reservas).rjust(5)} |")
        print("="*60)
        print("CRIADO POR:")
        print("-"*60)
        print(f"| {created_by:<80}            |")
        print("="*60)
        print("PROFESSOR:")
        print("-"*60)
        print(f"| {professor:<53} {coracao:<3} |")
        print("="*60)
        print("DISCIPLINA:")
        print("-"*60)
        print(f"| {disciplina:<49} {semestre:<1} |")
        print("="*60)

    except Exception as e:
        print(f"Ocorreu um erro ao exibir o menu principal: {e}")

def menu_principal(db_type):
    while True:
        print("\n" + "="*47)
        print(" "*9 + "SISTEMA DE GESTÃO DE HOTEL")
        print("="*47)

        # Ajustar termos conforme o banco de dados
        termo = "Documentos" if db_type == 'mongodb' else "Registros"

        print("\nSelecione uma opção:")
        print("-"*47)
        print(f"| 1.    📊  Relatórios                        |")
        print("-"*47)
        print(f"| 2.    ➕  Inserir {termo}                   |")
        print("-"*47)
        print(f"| 3.    🗑️   Remover {termo}                   |")
        print("-"*47)
        print(f"| 4.    ✏️   Atualizar {termo}                 |")
        print("-"*47)
        print(f"| 5.    ❌  Sair                              |")
        print("-"*47)
        print(f"| 6.    🔄  Mudar Banco de Dados              |")
        print("="*47)

        escolha = input("\nDigite sua opção: ")

        if escolha == '1':
            menu_relatorios(db_type)
        elif escolha == '2':
            menu_inserir_documentos(db_type, termo)
        elif escolha == '3':
            menu_remover_documentos(db_type, termo)
        elif escolha == '4':
            menu_atualizar_documentos(db_type, termo)
        elif escolha == '5':
            print("\nSaindo... Obrigado por utilizar o sistema!")
            print("="*47)
            break
        elif escolha == '6':
            db_type = escolher_banco_de_dados()
            menu_de_criacao(db_type)
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_relatorios(db_type):
    while True:
        print("\n" + "="*47)
        print(" "*15 + "MENU RELATÓRIOS")
        print("="*47)

        print("\nSelecione uma opção:")
        print("-"*47)
        print("| 1. 📊  Visão de Hotel                       |")
        print("-"*47)
        print("| 2. 🏨  Relatório de Quarto                  |")
        print("-"*47)
        print("| 3. 👤  Relatório de Clientes                |")
        print("-"*47)
        print("| 4. 📝  Relatório de Reservas                |")
        print("-"*47)
        print("| 5. 🔙  Voltar                               |")
        print("="*47)

        escolha = input("\nDigite sua opção: ")

        if escolha == '1':
            Relatorio.visao_de_hotel(db_type)
        elif escolha == '2':
            Relatorio.relatorio_quarto(db_type)
        elif escolha == '3':
            Relatorio.relatorio_clientes(db_type)
        elif escolha == '4':
            Relatorio.relatorio_reservas(db_type)
        elif escolha == '5':
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_inserir_documentos(db_type, termo):
    while True:
        print("\n" + "="*47)
        print(f" "*12 + f"INSERIR {termo.upper()}")
        print("="*47)
        print("\nSelecione uma opção:")
        print("-"*47)
        print("| 1. ➕  Inserir Cliente                      |")
        print("-"*47)
        print("| 2. ➕  Inserir Quarto                       |")
        print("-"*47)
        print("| 3. ➕  Inserir Reserva                      |")
        print("-"*47)
        print("| 4. 🔙  Voltar                               |")
        print("="*47)

        escolha = input("\nDigite sua opção: ")

        if escolha == '1':
            create_cliente(db_type)
        elif escolha == '2':
            create_quarto(db_type)
        elif escolha == '3':
            create_reserva(db_type)
        elif escolha == '4':
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_remover_documentos(db_type, termo):
    while True:
        print("\n" + "="*47)
        print(f" "*12 + f"REMOVER {termo.upper()}")
        print("="*47)
        print("\nSelecione uma opção:")
        print("-"*47)
        print("| 1. 🗑️   Remover Cliente                    |")
        print("-"*47)
        print("| 2. 🗑️   Remover Quarto                     |")
        print("-"*47)
        print("| 3. 🗑️   Remover Reserva                    |")
        print("-"*47)
        print("| 4. 🔙  Voltar                              |")
        print("="*47)

        escolha = input("\nDigite sua opção: ")

        if escolha == '1':
            delete_cliente(db_type)
        elif escolha == '2':
            delete_quarto(db_type)
        elif escolha == '3':
            delete_reserva(db_type)
        elif escolha == '4':
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def menu_atualizar_documentos(db_type, termo):
    while True:
        print("\n" + "="*47)
        print(f" "*12 + f"ATUALIZAR {termo.upper()}")
        print("="*47)
        print("\nSelecione uma opção:")
        print("-"*47)
        print("| 1. ✏️   Atualizar Cliente                  |")
        print("-"*47)
        print("| 2. ✏️   Atualizar Quarto                   |")
        print("-"*47)
        print("| 3. ✏️   Atualizar Reserva                  |")
        print("-"*47)
        print("| 4. 🔙  Voltar                              |")
        print("="*47)

        escolha = input("\nDigite sua opção: ")

        if escolha == '1':
            update_cliente(db_type)
        elif escolha == '2':
            update_quarto(db_type)
        elif escolha == '3':
            update_reserva(db_type)
        elif escolha == '4':
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def create_cliente(db_type):
    cpf = input("Informe o CPF: ").strip()
    if Cliente.cliente_exists(cpf, db_type):
        print("Cliente já cadastrado.")
        return

    nome = input("Informe o Nome: ").strip()
    email = input("Informe o Email: ").strip()
    telefone = input("Informe o Telefone: ").strip()
    data_nascimento = input("Informe a Data de Nascimento (DD-MM-YYYY): ").strip()
    try:
        data_nascimento_dt = datetime.datetime.strptime(data_nascimento, "%d-%m-%Y")
    except ValueError:
        print("Data de nascimento inválida.")
        return
    cep = input("Informe o CEP: ").strip()

    cliente = Cliente(cpf, telefone, nome, email, data_nascimento_dt, cep, db_type)
    cliente.create_cliente()
    print("Cliente cadastrado com sucesso.")

def create_quarto(db_type):
    num_quarto = input("Informe o Número do Quarto: ").strip()
    if Quarto.quarto_exists(num_quarto, db_type):
        print("Quarto já cadastrado.")
        return

    tipo_quarto = input("Informe o Tipo do Quarto: ").strip()
    valor_diaria = input("Informe o Valor da Diária: ").strip()
    try:
        valor_diaria = float(valor_diaria)
    except ValueError:
        print("Valor da diária inválido.")
        return
    limite_pessoas = input("Informe o Limite de Pessoas: ").strip()
    try:
        limite_pessoas = int(limite_pessoas)
    except ValueError:
        print("Limite de pessoas inválido.")
        return

    quarto = Quarto(num_quarto, tipo_quarto, valor_diaria, limite_pessoas, db_type=db_type)
    quarto.create_quarto()
    print("Quarto cadastrado com sucesso.")

def create_reserva(db_type):
    num_reserva = input("Informe o Número da Reserva: ").strip()

    cpf = input("Informe o CPF do cliente: ").strip()
    if not Cliente.cliente_exists(cpf, db_type):
        print("Cliente não encontrado.")
        return

    num_quarto = input("Informe o número do quarto: ").strip()
    if not Quarto.quarto_exists(num_quarto, db_type):
        print("Quarto não encontrado.")
        return

    while True:
        data_inicio = input("Informe a Data de Início (DD-MM-YYYY): ").strip()
        try:
            data_inicio_dt = datetime.datetime.strptime(data_inicio, "%d-%m-%Y")
            break
        except ValueError:
            print("Data inválida. Tente novamente.")

    while True:
        data_final = input("Informe a Data Final (DD-MM-YYYY): ").strip()
        try:
            data_final_dt = datetime.datetime.strptime(data_final, "%d-%m-%Y")
            if data_final_dt <= data_inicio_dt:
                print("A data final deve ser posterior à data de início.")
            else:
                break
        except ValueError:
            print("Data inválida. Tente novamente.")

    quantidade_pessoas = input("Informe a Quantidade de Pessoas: ").strip()
    try:
        quantidade_pessoas = int(quantidade_pessoas)
    except ValueError:
        print("Quantidade de pessoas inválida.")
        return

    cafe_incluso_opcao = input("Café incluso? (1 para Sim, 2 para Não): ").strip()
    cafe_incluso = cafe_incluso_opcao == '1'

    num_dias = (data_final_dt - data_inicio_dt).days
    valor_reserva = calcular_valor_reserva(num_quarto, num_dias, cafe_incluso, db_type)

    reserva = Reserva(num_reserva, data_inicio_dt, data_final_dt, quantidade_pessoas,
                      valor_reserva, cpf, num_quarto, cafe_incluso, db_type)
    reserva.create_reserva()

    # Atualizar o CPF no quarto
    quarto = Quarto(num_quarto=num_quarto, cpf=cpf, db_type=db_type)
    quarto.atualizar_cpf()

    print(f"\nReserva número {num_reserva} criada com sucesso! Valor total: R${valor_reserva:.2f} para {num_dias} dias.")

def calcular_valor_reserva(num_quarto, num_dias, cafe_incluso, db_type):
    if db_type == 'mysql':
        db = MySQLConnection()
        if not db.connected:
            print("Erro na conexão com o MySQL.")
            return 0
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT VALOR_DIARIA FROM QUARTO WHERE NUM_QUARTO = %s", (num_quarto,))
        result = cursor.fetchone()
        if result:
            valor_diaria = result[0]
        else:
            print("Quarto não encontrado.")
            return 0
        cursor.close()
        db.close_connection()
    elif db_type == 'mongodb':
        db = MongoDBConnection()
        if not db.connected:
            print("Erro na conexão com o MongoDB.")
            return 0
        collection = db.get_db()['quartos']
        quarto = collection.find_one({'num_quarto': num_quarto})
        if quarto:
            valor_diaria = quarto['valor_diaria']
        else:
            print("Quarto não encontrado.")
            return 0
        db.close_connection()
    else:
        print("Tipo de banco de dados inválido.")
        return 0

    valor_total = valor_diaria * num_dias
    if cafe_incluso:
        valor_total += 60  # Valor adicional para café da manhã

    return valor_total

def delete_cliente(db_type):
    cpf = input("Informe o CPF do Cliente que deseja deletar: ").strip()

    if not Cliente.cliente_exists(cpf, db_type):
        print("Cliente não encontrado.")
        return

    confirmar = input("Tem certeza que deseja deletar este cliente? (s/n): ").lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return

    cliente = Cliente(cpf=cpf, db_type=db_type)
    cliente.delete_cliente()
    print("Cliente deletado com sucesso.")

def delete_quarto(db_type):
    num_quarto = input("Informe o Número do Quarto que deseja deletar: ").strip()

    if not Quarto.quarto_exists(num_quarto, db_type):
        print("Quarto não encontrado.")
        return

    confirmar = input("Tem certeza que deseja deletar este quarto? (s/n): ").lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return

    quarto = Quarto(num_quarto=num_quarto, db_type=db_type)
    quarto.delete_quarto()
    print("Quarto deletado com sucesso.")

def delete_reserva(db_type):
    num_reserva = input("Informe o Número da Reserva que deseja deletar: ").strip()

    if not Reserva.reserva_exists(num_reserva, db_type):
        print("Reserva não encontrada.")
        return

    confirmar = input("Tem certeza que deseja deletar esta reserva? (s/n): ").lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return

    reserva = Reserva(num_reserva=num_reserva, db_type=db_type)
    reserva.delete_reserva()
    print("Reserva deletada com sucesso.")

    # Limpar o CPF do quarto associado
    num_quarto = reserva.num_quarto
    quarto = Quarto(num_quarto=num_quarto, cpf=None, db_type=db_type)
    quarto.atualizar_cpf()
    print(f"O quarto {num_quarto} está agora disponível.")

def update_cliente(db_type):
    cpf = input("Informe o CPF do cliente que deseja atualizar: ").strip()

    if not Cliente.cliente_exists(cpf, db_type):
        print("Cliente não encontrado.")
        return

    telefone = input("Informe o novo Telefone (deixe em branco para manter): ").strip()
    nome = input("Informe o novo Nome (deixe em branco para manter): ").strip()
    email = input("Informe o novo Email (deixe em branco para manter): ").strip()
    data_nascimento = input("Informe a nova Data de Nascimento (DD-MM-YYYY) (deixe em branco para manter): ").strip()
    data_nascimento_dt = None
    if data_nascimento:
        try:
            data_nascimento_dt = datetime.datetime.strptime(data_nascimento, "%d-%m-%Y")
        except ValueError:
            print("Data inválida. Tente novamente.")
            return
    cep = input("Informe o novo CEP (deixe em branco para manter): ").strip()

    cliente = Cliente(cpf, telefone or None, nome or None, email or None, data_nascimento_dt, cep or None, db_type)
    cliente.update_cliente()
    print("Cliente atualizado com sucesso.")

def update_quarto(db_type):
    num_quarto = input("Informe o Número do Quarto que deseja atualizar: ").strip()

    if not Quarto.quarto_exists(num_quarto, db_type):
        print("Quarto não encontrado.")
        return

    tipo_quarto = input("Informe o novo Tipo do Quarto (deixe em branco para manter): ").strip()
    valor_diaria = input("Informe o novo Valor da Diária (deixe em branco para manter): ").strip()
    limite_pessoas = input("Informe o novo Limite de Pessoas (deixe em branco para manter): ").strip()

    quarto = Quarto(num_quarto, tipo_quarto or None, float(valor_diaria) if valor_diaria else None,
                    limite_pessoas or None, db_type=db_type)
    quarto.update_quarto()
    print("Quarto atualizado com sucesso.")

def update_reserva(db_type):
    num_reserva = input("Informe o Número da Reserva que deseja atualizar: ").strip()

    if not Reserva.reserva_exists(num_reserva, db_type):
        print("Reserva não encontrada.")
        return

    cpf = input("Informe o novo CPF do cliente (deixe em branco para manter): ").strip()
    num_quarto = input("Informe o novo número do quarto (deixe em branco para manter): ").strip()
    data_inicio = input("Informe a nova Data de Início (DD-MM-YYYY) (deixe em branco para manter): ").strip()
    data_inicio_dt = None
    if data_inicio:
        try:
            data_inicio_dt = datetime.datetime.strptime(data_inicio, "%d-%m-%Y")
        except ValueError:
            print("Data inválida. Tente novamente.")
            return
    data_final = input("Informe a nova Data Final (DD-MM-YYYY) (deixe em branco para manter): ").strip()
    data_final_dt = None
    if data_final:
        try:
            data_final_dt = datetime.datetime.strptime(data_final, "%d-%m-%Y")
            if data_inicio_dt and data_final_dt <= data_inicio_dt:
                print("A data final deve ser posterior à data de início.")
                return
        except ValueError:
            print("Data inválida. Tente novamente.")
            return
    quantidade_pessoas = input("Informe a nova Quantidade de Pessoas (deixe em branco para manter): ").strip()
    cafe_incluso_opcao = input("Café incluso? (1 para Sim, 2 para Não, deixe em branco para manter): ").strip()
    cafe_incluso = None
    if cafe_incluso_opcao == '1':
        cafe_incluso = True
    elif cafe_incluso_opcao == '2':
        cafe_incluso = False

    reserva = Reserva(num_reserva, data_inicio_dt, data_final_dt, quantidade_pessoas or None,
                      None, cpf or None, num_quarto or None, cafe_incluso, db_type)
    reserva.update_reserva()
    print("Reserva atualizada com sucesso.")

if __name__ == "__main__":
    db_type = escolher_banco_de_dados()
    menu_de_criacao(db_type)
    menu_principal(db_type)
