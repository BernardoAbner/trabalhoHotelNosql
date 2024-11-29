# VIEWS/relatorio_view.py

from CONTROLLERS.relatorio_controller import RelatorioController

class RelatorioView:
    @staticmethod
    def gerar_visao_de_hotel(db_type='mongodb'):
        print("Chamando relatório de visão de hotel...")
        RelatorioController.gerar_visao_de_hotel(db_type)
    
    @staticmethod
    def gerar_relatorio_quarto(db_type='mongodb'):
        print("Chamando relatório de quarto...")
        RelatorioController.gerar_relatorio_quarto(db_type)
    
    @staticmethod
    def gerar_relatorio_cliente(db_type='mongodb'):
        print("Chamando relatório de cliente...")
        RelatorioController.gerar_relatorio_cliente(db_type)
    
    @staticmethod
    def gerar_relatorio_reserva(db_type='mongodb'):
        print("Chamando relatório de reserva...")
        RelatorioController.gerar_relatorio_reserva(db_type)
    
    @staticmethod
    def gerar_relatorio_menu(db_type='mongodb'):
        while True:
            print("\n" + "="*47)
            print(f"{'MENU RELATÓRIOS':^47}")
            print("="*47)
            options = {
                '1': '📊  Visão de Hotel',
                '2': '🏨  Relatório de Quarto',
                '3': '👤  Relatório de cliente',
                '4': '📝  Relatório de reserva',
                '5': '🔙  Voltar'
            }
            print("\nSelecione uma opção:")
            for key, value in options.items():
                print(f"{key}. {value}")
            choice = input("Digite sua opção: ")
            print(f"Opção escolhida: {choice}")  # Debug print
            if choice == '1':
                RelatorioController.gerar_visao_de_hotel(db_type)
            elif choice == '2':
                RelatorioController.gerar_relatorio_quarto(db_type)
            elif choice == '3':
                RelatorioController.gerar_relatorio_cliente(db_type)
            elif choice == '4':
                RelatorioController.gerar_relatorio_reserva(db_type)
            elif choice == '5':
                print("Voltando ao menu principal.")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
