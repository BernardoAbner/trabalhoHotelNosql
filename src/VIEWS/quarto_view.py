# views/quarto_view.py

from CONTROLLERS.quarto_controller import QuartoController

class QuartoView:
    @staticmethod
    def criar_quarto():
        while True:
            num_quarto = input("Informe o Número do Quarto: ").strip()
            tipo_quarto = input("Informe o Tipo do Quarto: ").strip()
            valor_diaria = input("Informe o Valor da Diária: ").strip()
            try:
                valor_diaria = float(valor_diaria)
            except ValueError:
                print("Valor da diária inválido.")
                continue
            limite_pessoas = input("Informe o Limite de Pessoas: ").strip()
            try:
                limite_pessoas = int(limite_pessoas)
            except ValueError:
                print("Limite de pessoas inválido.")
                continue
            QuartoController.criar_quarto(num_quarto, tipo_quarto, valor_diaria, limite_pessoas)

            # Perguntar se deseja continuar inserindo registros
            continuar = input("Deseja inserir outro quarto? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de inclusão de quartos.")
                break

    @staticmethod
    def atualizar_quarto():
        while True:
            num_quarto = input("Informe o Número do Quarto que deseja atualizar: ").strip()

            # Confirmação antes de atualizar
            confirmacao = input(f"Tem certeza que deseja atualizar o quarto número {num_quarto}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação de atualização cancelada.")
                break

            print("Deixe os campos em branco se não quiser alterar.")
            tipo_quarto = input("Informe o novo Tipo do Quarto: ").strip()
            valor_diaria = input("Informe o novo Valor da Diária: ").strip()
            limite_pessoas = input("Informe o novo Limite de Pessoas: ").strip()
            cpf = input("Informe o CPF do Hóspede (deixe em branco para liberar o quarto): ").strip()

            valor_diaria = float(valor_diaria) if valor_diaria else None
            limite_pessoas = int(limite_pessoas) if limite_pessoas else None

            QuartoController.atualizar_quarto(
                num_quarto,
                tipo_quarto if tipo_quarto else None,
                valor_diaria,
                limite_pessoas,
                cpf if cpf else None
            )

            # Pergunta se o usuário deseja continuar atualizando registros
            continuar = input("Deseja continuar atualizando quartos? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de atualização de quartos.")
                break
            
    @staticmethod
    def deletar_quarto():
        while True:
            num_quarto = input("Informe o Número do Quarto que deseja deletar: ").strip()

            # Confirmação antes de deletar
            confirmacao = input(f"Tem certeza que deseja deletar o quarto número {num_quarto}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação de exclusão cancelada.")
                break

            QuartoController.deletar_quarto(num_quarto)

            # Pergunta se o usuário deseja continuar deletando
            continuar = input("Deseja continuar deletando quartos? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de exclusão de quartos.")
                break

    @staticmethod
    def listar_quarto():
        QuartoController.listar_quarto()
