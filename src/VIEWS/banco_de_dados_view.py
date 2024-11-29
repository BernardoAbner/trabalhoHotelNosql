# views/banco_de_dados_view.py

def selecionar_banco_de_dados():
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
