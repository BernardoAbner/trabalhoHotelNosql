# CONTROLLERS/relatorio_controller.py

from MODELS.relatorio import Relatorio

class RelatorioController:
    @staticmethod
    def gerar_visao_de_hotel(db_type='mongodb'):
        Relatorio.visao_de_hotel(db_type)
    
    @staticmethod
    def gerar_relatorio_quarto(db_type='mongodb'):
        Relatorio.relatorio_quarto(db_type)
    
    @staticmethod
    def gerar_relatorio_cliente(db_type='mongodb'):
        Relatorio.relatorio_cliente(db_type)
    
    @staticmethod
    def gerar_relatorio_reserva(db_type='mongodb'):
        Relatorio.relatorio_reserva(db_type)
    
    @staticmethod
    def listar_todos_cliente(db_type='mongodb'):
        Relatorio.listar_todos_cliente(db_type)
    
    @staticmethod
    def listar_todas_reserva(db_type='mongodb'):
        Relatorio.listar_todas_reserva(db_type)
