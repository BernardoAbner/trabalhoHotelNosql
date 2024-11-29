# controllers/cliente_controller.py

from MODELS.cliente import Cliente
import datetime

class ClienteController:
    @staticmethod
    def criar_cliente(cpf, nome, email, telefone, data_nascimento_str, cep, db_type='mongodb'):
        """
        Cria um novo cliente no banco de dados selecionado.
        """
        try:
            data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%d-%m-%Y")
        except ValueError:
            print("Formato de data inválido. Use DD-MM-YYYY.")
            return

        if Cliente.cliente_exists(cpf, db_type):
            print("Cliente já cadastrado.")
            return

        cliente = Cliente(cpf, nome, email, telefone, data_nascimento, cep, db_type)
        cliente.create_cliente()

    @staticmethod
    def atualizar_cliente(cpf, nome=None, email=None, telefone=None, data_nascimento_str=None, cep=None, db_type='mongodb'):
        """
        Atualiza as informações de um cliente existente.
        """
        data_nascimento = None
        if data_nascimento_str:
            try:
                data_nascimento = datetime.datetime.strptime(data_nascimento_str, "%d-%m-%Y")
            except ValueError:
                print("Formato de data inválido. Use DD-MM-YYYY.")
                return

        if not Cliente.cliente_exists(cpf, db_type):
            print("Cliente não encontrado.")
            return

        cliente = Cliente(cpf, nome, email, telefone, data_nascimento, cep, db_type)
        cliente.update_cliente(nome, email, telefone, data_nascimento, cep)

    @staticmethod
    def deletar_cliente(cpf, db_type='mongodb'):
        """
        Remove um cliente do banco de dados selecionado.
        """
        if not Cliente.cliente_exists(cpf, db_type):
            print("Cliente não encontrado.")
            return

        cliente = Cliente(cpf, None, None, None, None, None, db_type)
        cliente.delete_cliente()
        print(f"Cliente com CPF {cpf} deletado com sucesso.")
        
    @staticmethod
    def listar_cliente(db_type='mongodb'):
        """
        Lista todos os cliente cadastrados.
        """
        total = Cliente.get_total_cliente(db_type)
        print(f"Total de cliente: {total}")
        Cliente.listar_todos_cliente(db_type)
