# main.py

from VIEWS.main_view import MainView
from VIEWS.banco_de_dados_view import selecionar_banco_de_dados
from VIEWS.menu_de_criacao_view import MenuDeCriacaoView

def main():
    db_type = selecionar_banco_de_dados()
    MenuDeCriacaoView.exibir_menu(db_type)
    MainView.run(db_type)

if __name__ == "__main__":
    main()
