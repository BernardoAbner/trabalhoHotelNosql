# controllers/quarto_controller.py

from MODELS.quarto import Quarto

class QuartoController:
    @staticmethod
    def criar_quarto(num_quarto, tipo_quarto, valor_diaria, limite_pessoas, db_type='mongodb'):
        """
        Cria um novo quarto no banco de dados selecionado.
        """
        if Quarto.quarto_exists(num_quarto, db_type):
            print("Quarto já cadastrado.")
            return
        quarto = Quarto(num_quarto, tipo_quarto, valor_diaria, limite_pessoas, db_type=db_type)
        quarto.create_quarto()

    @staticmethod
    def atualizar_quarto(num_quarto, tipo_quarto=None, valor_diaria=None, limite_pessoas=None, cpf=None, db_type='mongodb'):
        """
        Atualiza as informações de um quarto existente.
        """
        if not Quarto.quarto_exists(num_quarto, db_type):
            print("Quarto não encontrado.")
            return
        quarto = Quarto(num_quarto, tipo_quarto, valor_diaria, limite_pessoas, cpf, db_type=db_type)
        quarto.update_quarto(tipo_quarto, valor_diaria, limite_pessoas, cpf)

    @staticmethod
    def deletar_quarto(num_quarto, db_type='mongodb'):
        """
        Remove um quarto do banco de dados selecionado.
        """
        if not Quarto.quarto_exists(num_quarto, db_type):
            print("Quarto não encontrado.")
            return

        quarto = Quarto(num_quarto, None, None, None, db_type=db_type)
        quarto.delete_quarto()
        print(f"Quarto número {num_quarto} deletado com sucesso.")

    @staticmethod
    def listar_quarto(db_type='mongodb'):
        """
        Lista todos os quarto cadastrados.
        """
        total = Quarto.get_total_quarto(db_type)
        print(f"Total de quarto: {total}")
        Quarto.listar_todos_quarto(db_type)
