# views/reserva_view.py

from CONTROLLERS.reserva_controller import ReservaController

class ReservaView:
    @staticmethod
    def criar_reserva():
        while True:
            num_reserva = input("Informe o Número da Reserva: ").strip()
            cpf = input("Informe o CPF do cliente: ").strip()
            num_quarto = input("Informe o número do quarto: ").strip()
            data_inicio = input("Informe a Data de Início (DD-MM-YYYY): ").strip()
            data_final = input("Informe a Data Final (DD-MM-YYYY): ").strip()
            quantidade_pessoas = input("Informe a Quantidade de Pessoas: ").strip()
            try:
                quantidade_pessoas = int(quantidade_pessoas)
            except ValueError:
                print("Quantidade de pessoas inválida.")
                return
            cafe_incluso_opcao = input("Café incluso? (1 para Sim, 2 para Não): ").strip()
            cafe_incluso = True if cafe_incluso_opcao == '1' else False

            ReservaController.criar_reserva(
                num_reserva,
                cpf,
                num_quarto,
                data_inicio,
                data_final,
                quantidade_pessoas,
                cafe_incluso
            )

            continuar = input("Deseja continuar inserindo reservas? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de criação de reservas.")
                break

    @staticmethod
    def atualizar_reserva():
        while True:
            num_reserva = input("Informe o Número da Reserva que deseja atualizar: ").strip()

            # Confirmação antes de atualizar
            confirmacao = input(f"Tem certeza que deseja atualizar a reserva número {num_reserva}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação de atualização cancelada.")
                break

            print("Deixe os campos em branco se não quiser alterar.")
            cpf = input("Informe o novo CPF do cliente: ").strip()
            num_quarto = input("Informe o novo número do quarto: ").strip()
            data_inicio = input("Informe a nova Data de Início (DD-MM-YYYY): ").strip()
            data_final = input("Informe a nova Data Final (DD-MM-YYYY): ").strip()
            quantidade_pessoas = input("Informe a nova Quantidade de Pessoas: ").strip()
            cafe_incluso_opcao = input("Café incluso? (1 para Sim, 2 para Não): ").strip()
            cafe_incluso = None
            if cafe_incluso_opcao == '1':
                cafe_incluso = True
            elif cafe_incluso_opcao == '2':
                cafe_incluso = False

            ReservaController.atualizar_reserva(
                num_reserva,
                cpf if cpf else None,
                num_quarto if num_quarto else None,
                data_inicio if data_inicio else None,
                data_final if data_final else None,
                int(quantidade_pessoas) if quantidade_pessoas else None,
                cafe_incluso,
            )

            # Pergunta se o usuário deseja continuar atualizando registros
            continuar = input("Deseja continuar atualizando reservas? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de atualização de reservas.")
                break

    @staticmethod
    def deletar_reserva():
        while True:
            num_reserva = input("Informe o Número da Reserva que deseja deletar: ").strip()

            # Confirmação antes de deletar
            confirmacao = input(f"Tem certeza que deseja deletar a reserva número {num_reserva}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação de exclusão cancelada.")
                break

            ReservaController.deletar_reserva(num_reserva)

            # Pergunta se o usuário deseja continuar deletando
            continuar = input("Deseja continuar deletando reservas? (s/n): ").strip().lower()
            if continuar != 's':
                print("Saindo do submenu de exclusão de reservas.")
                break

    @staticmethod
    def listar_reserva():
        ReservaController.listar_reserva()
