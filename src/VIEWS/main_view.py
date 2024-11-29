# VIEWS/main_view.py

from VIEWS.cliente_view import ClienteView
from VIEWS.quarto_view import QuartoView
from VIEWS.reserva_view import ReservaView
from VIEWS.relatorio_view import RelatorioView
from VIEWS.banco_de_dados_view import selecionar_banco_de_dados

class MainView:
    @staticmethod
    def display_menu():
        print("\n" + "="*60)
        print(f"{'SISTEMA DE GESTÃO DE HOTEL':^60}")
        print("="*60)

    @staticmethod
    def get_user_choice(options):
        print("\nSelecione uma opção:")
        print("-"*60)
        for key, value in options.items():
            print(f"| {key}. {value:<52} |")
            print("-"*60)
        choice = input("\nDigite sua opção: ")
        return choice

    @staticmethod
    def run(db_type='mongodb'):
        while True:
            MainView.display_menu()
            options = {
                '1': '📊  Relatórios',
                '2': '➕  Inserir Documentos',
                '3': '🗑️   Remover Documentos',
                '4': '✏️   Atualizar Documentos',
                '5': '❌  Sair',
                '6': '🔄  Mudar Banco de Dados'
            }
            choice = MainView.get_user_choice(options)

            if choice == '1':
                RelatorioView.gerar_relatorio_menu(db_type)
            elif choice == '2':
                MainView.inserir_documentos_menu(db_type)
            elif choice == '3':
                MainView.remover_documentos_menu(db_type)
            elif choice == '4':
                MainView.atualizar_documentos_menu(db_type)
            elif choice == '5':
                print("\nSaindo... Obrigado por utilizar o sistema!")
                print("="*60)
                break
            elif choice == '6':
                db_type = selecionar_banco_de_dados()
            else:
                print("\nOpção inválida. Tente novamente.")

    @staticmethod
    def inserir_documentos_menu(db_type):
        print("\n" + "="*47)
        print(f"{'INSERIR DOCUMENTOS':^47}")
        print("="*47)
        options = {
            '1': '➕  Inserir Cliente',
            '2': '➕  Inserir Quarto',
            '3': '➕  Inserir Reserva',
            '4': '🔙  Voltar'
        }
        while True:
            choice = MainView.get_user_choice(options)
            if choice == '1':
                ClienteView.criar_cliente()
            elif choice == '2':
                QuartoView.criar_quarto()
            elif choice == '3':
                ReservaView.criar_reserva()
            elif choice == '4':
                break
            else:
                print("\nOpção inválida. Tente novamente.")

    @staticmethod
    def remover_documentos_menu(db_type):
        print("\n" + "="*47)
        print(f"{'REMOVER DOCUMENTOS':^47}")
        print("="*47)
        options = {
            '1': '🗑️   Remover Cliente',
            '2': '🗑️   Remover Quarto',
            '3': '🗑️   Remover Reserva',
            '4': '🔙  Voltar'
        }
        while True:
            choice = MainView.get_user_choice(options)
            if choice == '1':
                ClienteView.deletar_cliente()
            elif choice == '2':
                QuartoView.deletar_quarto()
            elif choice == '3':
                ReservaView.deletar_reserva()
            elif choice == '4':
                break
            else:
                print("\nOpção inválida. Tente novamente.")

    @staticmethod
    def atualizar_documentos_menu(db_type):
        print("\n" + "="*47)
        print(f"{'ATUALIZAR DOCUMENTOS':^47}")
        print("="*47)
        options = {
            '1': '✏️   Atualizar Cliente',
            '2': '✏️   Atualizar Quarto',
            '3': '✏️   Atualizar Reserva',
            '4': '🔙  Voltar'
        }
        while True:
            choice = MainView.get_user_choice(options)
            if choice == '1':
                ClienteView.atualizar_cliente()
            elif choice == '2':
                QuartoView.atualizar_quarto()
            elif choice == '3':
                ReservaView.atualizar_reserva()
            elif choice == '4':
                break
            else:
                print("\nOpção inválida. Tente novamente.")
