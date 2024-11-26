

from mongodb_connection import DatabaseConnection

def initialize_database():
    db = DatabaseConnection().get_db()

    # Coleção de Clientes
    clientes_collection = db['clientes']
    clientes_collection.create_index('cpf', unique=True)
    print("Índice único criado na coleção 'clientes' para o campo 'cpf'.")

    # Coleção de Quartos
    quartos_collection = db['quartos']
    quartos_collection.create_index('num_quarto', unique=True)
    print("Índice único criado na coleção 'quartos' para o campo 'num_quarto'.")

    # Coleção de Reservas
    reservas_collection = db['reservas']
    reservas_collection.create_index('num_reserva', unique=True)
    print("Índice único criado na coleção 'reservas' para o campo 'num_reserva'.")

    # Índice adicional em 'cpf' na coleção 'reservas' para melhorar as consultas
    reservas_collection.create_index('cpf')
    print("Índice criado na coleção 'reservas' para o campo 'cpf'.")

    # Índice adicional em 'num_quarto' na coleção 'reservas' para melhorar as consultas
    reservas_collection.create_index('num_quarto')
    print("Índice criado na coleção 'reservas' para o campo 'num_quarto'.")

    # Fechar a conexão
    DatabaseConnection().close_connection()
    print("Configuração do banco de dados concluída.")

if __name__ == "__main__":
    initialize_database()
