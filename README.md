
# Sistema de Gerenciamento de Hotel

Este projeto é um sistema de gerenciamento de hotel desenvolvido em Python, utilizando MongoDB para armazenamento de dados. 
O objetivo do sistema é gerenciar clientes, quartos, reservas e gerar relatórios.

## Estrutura do Projeto

- **`cliente.py`**: Gerencia os dados e operações relacionadas aos clientes.
- **`main.py`**: Arquivo principal para execução do sistema.
- **`mongodb_connection.py`**: Configuração e gerenciamento da conexão com o banco de dados MongoDB.
- **`mysql_connection.py`**: (Opcional) Integração com MySQL, caso necessário.
- **`quarto.py`**: Gerencia os dados dos quartos.
- **`relatorio.py`**: Geração de relatórios relacionados ao sistema.
- **`reserva.py`**: Manipulação de reservas de clientes nos quartos.
- **`script_mongodb.py`**: Scripts adicionais para operações no MongoDB.

## Requisitos

- **Sistema Operacional**: Linux (Red Hat ou outras distribuições).
- **Linguagens**: Python 3.8 ou superior.
- **Banco de Dados**: MongoDB.

## Configuração do Ambiente

1. **Instale o Python**:
   ```bash
   sudo yum install python3
   ```

2. **Instale o MongoDB**:
   Siga a [documentação oficial do MongoDB](https://www.mongodb.com/docs/manual/installation/) para Red Hat.

3. **Instale as dependências do projeto**:
   No diretório raiz do projeto, execute:
   ```bash
   pip3 install -r requirements.txt
   ```

   Certifique-se de adicionar um arquivo `requirements.txt` com as bibliotecas necessárias, como `pymongo`.

4. **Configuração do MongoDB**:
   Certifique-se de que o MongoDB está em execução e que as credenciais de conexão no arquivo `mongodb_connection.py` estão corretas.

## Execução do Projeto

1. Certifique-se de que o MongoDB está ativo:
   ```bash
   sudo systemctl start mongod
   ```

2. Execute o sistema:
   ```bash
   python3 main.py
   ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
