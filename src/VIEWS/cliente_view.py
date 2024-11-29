# views/cliente_view.py

from CONTROLLERS.cliente_controller import ClienteController

class ClienteView:
    @staticmethod
    def criar_cliente():
        while True:
            cpf = input("Informe o CPF: ").strip()
            nome = input("Informe o Nome: ").strip()
            email = input("Informe o Email: ").strip()
            telefone = input("Informe o Telefone: ").strip()
            data_nascimento = input("Informe a Data de Nascimento (DD-MM-YYYY): ").strip()
            cep = input("Informe o CEP: ").strip()
            ClienteController.criar_cliente(cpf, nome, email, telefone, data_nascimento, cep)

            # Perguntar se deseja continuar inserindo registros
            continuar = input("Deseja inserir outro cliente? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de inclusão de clientes.")
                break

    @staticmethod
    def atualizar_cliente():
        while True:
            cpf = input("Informe o CPF do cliente que deseja atualizar: ").strip()

            # Confirmação antes de atualizar
            confirmacao = input(f"Tem certeza que deseja atualizar os dados do cliente com CPF {cpf}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação de atualização cancelada.")
                break

            print("Deixe os campos em branco se não quiser alterar.")
            nome = input("Informe o novo Nome: ").strip()
            email = input("Informe o novo Email: ").strip()
            telefone = input("Informe o novo Telefone: ").strip()
            data_nascimento = input("Informe a nova Data de Nascimento (DD-MM-YYYY): ").strip()
            cep = input("Informe o novo CEP: ").strip()

            ClienteController.atualizar_cliente(
                cpf,
                nome if nome else None,
                email if email else None,
                telefone if telefone else None,
                data_nascimento if data_nascimento else None,
                cep if cep else None
            )

            # Pergunta se o usuário deseja continuar atualizando
            continuar = input("Deseja continuar atualizando clientes? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de atualização de clientes.")
                break

    @staticmethod
    def deletar_cliente():
        while True:
            cpf = input("Informe o CPF do Cliente que deseja deletar: ").strip()

            # Confirmação antes de deletar
            confirmacao = input(f"Tem certeza que deseja deletar o cliente com CPF {cpf}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação de exclusão cancelada.")
                break

            ClienteController.deletar_cliente(cpf)

            # Pergunta se o usuário deseja continuar deletando
            continuar = input("Deseja continuar deletando clientes? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de exclusão de clientes.")
                break


    @staticmethod
    def listar_cliente():
        ClienteController.listar_cliente()
