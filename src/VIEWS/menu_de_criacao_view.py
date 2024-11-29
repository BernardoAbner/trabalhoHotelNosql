# VIEWS/menu_de_criacao_view.py
from MODELS.cliente import Cliente
from MODELS.quarto import Quarto
from MODELS.reserva import Reserva

class MenuDeCriacaoView:
    @staticmethod
    def exibir_menu(db_type):
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
