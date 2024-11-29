
# Sistema de Gerenciamento de Hotel

Este projeto é um sistema de gerenciamento de hotel desenvolvido em **Python**, com suporte a **MongoDB** e **MySQL** para armazenamento de dados. Ele gerencia clientes, quartos, reservas e permite a geração de relatórios.

---

## 📽️ Vídeo de Demonstração  
*(https://youtu.be/6TVy017h95Y?feature=shared)*  

---

## 📂 Estrutura do Projeto

### **`models/`**
- **`cliente.py`**: Gerencia os dados e operações relacionadas aos clientes.
- **`quarto.py`**: Gerencia os dados dos quartos.
- **`reserva.py`**: Manipula as reservas dos clientes nos quartos.
- **`relatorio.py`**: Gera relatórios relacionados ao sistema.

### **`DB Connections/`**
- **`mongodb_connection.py`**: Configura e gerencia a conexão com o banco de dados MongoDB.
- **`mysql_connection.py`**: Configura e gerencia a conexão com o banco de dados MySQL.

### **`controllers/`**
- **`cliente_controller.py`**: Gerencia operações relacionadas a clientes.
- **`quarto_controller.py`**: Lida com operações relacionadas a quartos.
- **`reserva_controller.py`**: Lida com operações de reserva.
- **`relatorio_controller.py`**: Gera e gerencia relatórios do sistema.

### **`utils/`**
- **`helpers.py`**: Funções auxiliares, como validação de dados e manipulação de datas.

### **`views/`**
- **`banco_de_dados_view.py`**: Interface para seleção do banco de dados.
- **`cliente_view.py`**: Interface de visualização e interação com clientes.
- **`main_view.py`**: Menu principal do sistema.
- **`menu_de_criacao_view.py`**: Exibe informações sobre a criação do sistema.
- **`quarto_view.py`**: Interface de visualização e interação com quartos.
- **`relatorio_view.py`**: Interface de visualização e interação com relatórios.
- **`reserva_view.py`**: Interface de visualização e interação com reservas.

### **`main.py`**
Ponto de entrada principal do sistema.

---

## ⚙️ Requisitos

### **Sistema Operacional**  
- **Linux**: Distribuição Red Hat ou outras compatíveis.

### **Linguagem**  
- **Python**: Versão 3.8 ou superior.

### **Banco de Dados**  
- **MongoDB** ou **MySQL** (configurável).

---

## 🚀 Configuração do Ambiente

### 1. **Instale o Python**  
Execute o comando:  
```bash
sudo yum install python3
```

### 2. **Instale o Banco de Dados**  
- **MongoDB**: Siga a [documentação oficial do MongoDB](https://www.mongodb.com/pt-br/docs/manual/installation/) para Red Hat.  
- **MySQL**: Siga a [documentação oficial do MySQL](https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/?form=MG0AV3).

### 3. **Instale as Dependências**  
No diretório raiz do projeto, execute:  
```bash
pip3 install -r requirements.txt
```

### 4. **Configuração do Banco de Dados**  
Certifique-se de que as credenciais de conexão estão corretas:  
- **MongoDB**: Ajuste `mongodb_connection.py` conforme necessário.  
- **MySQL**: Ajuste `mysql_connection.py` conforme necessário.  

---

## ▶️ Execução do Sistema

1. **Certifique-se de que o banco de dados está em execução**:  
   - **MongoDB**:  
     ```bash
     sudo systemctl start mongod
     ```  
   - **MySQL**:  
     ```bash
     sudo systemctl start mysqld
     ```  

2. **Inicie o sistema**:  
   ```bash
   python3 main.py
   ```

---

## 📊 Funcionalidades Principais

- **Gerenciamento de Clientes**: Cadastro, atualização e remoção de clientes.  
- **Gerenciamento de Quartos**: Controle dos dados dos quartos disponíveis e ocupados.  
- **Reservas**: Criação e gerenciamento de reservas.  
- **Relatórios**: Geração de relatórios de ocupação e reservas.  

---

## 🤝 Contribuição

Contribuições são bem-vindas!  
- Abra uma **issue** para relatar problemas ou sugerir melhorias.  
- Envie um **pull request** com as alterações propostas.  

---

## 📝 Licença  

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.  

---  
