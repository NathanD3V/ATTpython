# Gerenciador de Biodigestor com Interface Gráfica

Este projeto é uma aplicação de desktop desenvolvida em Python utilizando a biblioteca `tkinter` para a interface gráfica e `mysql.connector` para a conexão com um banco de dados MySQL. A aplicação permite o gerenciamento de um biodigestor, incluindo a inserção, visualização e remoção de dados relacionados a crioprotetores, além de fornecer um gráfico de capacidade em tempo real.

## Funcionalidades Principais

### 1. **Login de Usuário**
   - **Autenticação**: Os usuários podem fazer login fornecendo um nome de usuário e senha. O sistema verifica as credenciais no banco de dados e redireciona o usuário para a janela principal.
   - **Controle de Acesso**: Dependendo da função do usuário (`admin` ou `user`), ele terá acesso a diferentes funcionalidades.

### 2. **Gerenciamento de Biodigestor**
   - **Inserção de Dados**: Permite adicionar informações sobre crioprotetores, como nome, temperatura e quantidade. O sistema valida se a quantidade inserida não excede o limite máximo de 1000 unidades.
   - **Visualização de Dados**: Exibe todos os dados armazenados no banco de dados relacionados aos crioprotetores.
   - **Remoção de Dados**: Permite deletar registros de crioprotetores com base no nome.

### 3. **Gráfico de Capacidade**
   - **Atualização em Tempo Real**: Um gráfico de pizza exibe a capacidade atual do biodigestor, mostrando a quantidade ocupada e a quantidade disponível.
   - **Limite Máximo**: O gráfico respeita o limite máximo de 1000 unidades, alertando o usuário caso a inserção de dados exceda esse valor.

### 4. **Gerenciamento de Usuários (Apenas para Admin)**
   - **Adicionar Funcionário**: Permite ao administrador adicionar novos usuários ao sistema, definindo nome de usuário, senha e função.
   - **Visualizar Usuários**: Exibe todos os usuários cadastrados no sistema.
   - **Deletar Usuário**: Permite ao administrador remover usuários do sistema.

## Requisitos para Execução

### 1. **Banco de Dados MySQL**
   - **Criação do Banco de Dados e Tabelas**:
     Para que o código funcione corretamente, é necessário criar o banco de dados e as tabelas no MySQL. Execute os seguintes comandos:

     ```sql
     CREATE DATABASE bancopy;
     USE bancopy;

     CREATE TABLE tb_usuarios (
         id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(50) NOT NULL UNIQUE,
         senha VARCHAR(50) NOT NULL,
         role ENUM('admin', 'user') NOT NULL
     );

     CREATE TABLE tb_crioprotetores (
         id INT AUTO_INCREMENT PRIMARY KEY,
         crioprotetores VARCHAR(100) NOT NULL,
         temperatura VARCHAR(50) NOT NULL,
         quantidade INT NOT NULL,
         usuario_id INT,
         FOREIGN KEY (usuario_id) REFERENCES tb_usuarios(id)
     );
     ```

   - **Inserção de Dados de Exemplo**:
     Para facilitar o teste, insira alguns dados de exemplo:

     ```sql
     INSERT INTO tb_usuarios (username, senha, role) VALUES ('admin', '12345', 'admin');
     INSERT INTO tb_usuarios (username, senha, role) VALUES ('user1', '12345', 'user');
     ```

### 2. **Dependências do Python**
   - **Instalação das Bibliotecas Necessárias**:
     Para executar o código, instale as seguintes bibliotecas usando o pip:

     ```bash
     pip install tk
     pip install mysql-connector-python
     pip install matplotlib
     ```

### 3. **Configuração da Senha do Banco de Dados**
   - **Manutenção ou Alteração da Senha**:
     O código está configurado para usar a senha `12345` para acessar o banco de dados. Se você alterou a senha no MySQL, certifique-se de atualizar a senha no código na função `conectar_banco()`.

## Estrutura do Código

- **Conexão com o Banco de Dados**: A função `conectar_banco()` estabelece a conexão com o banco de dados MySQL.
- **Interface Gráfica**: A interface é construída usando `tkinter`, com janelas separadas para login, gerenciamento de biodigestor e gerenciamento de usuários.
- **Gráficos**: A biblioteca `matplotlib` é utilizada para gerar o gráfico de capacidade, que é exibido na janela principal.

## Como Executar

1. **Configuração do Banco de Dados**:
   - Certifique-se de que o MySQL está instalado e em execução.
   - Crie o banco de dados e as tabelas conforme os comandos fornecidos acima.

2. **Instalação das Dependências**:
   - Instale as bibliotecas necessárias usando pip:
     ```bash
     pip install tk mysql-connector-python matplotlib
     ```

3. **Execução do Programa**:
   - Execute o script Python:
     ```bash
     python nome_do_arquivo.py
     ```

## Considerações Finais

Este projeto é uma solução simples e eficaz para o gerenciamento de um biodigestor, com uma interface amigável e funcionalidades básicas de CRUD (Create, Read, Update, Delete). Ele pode ser expandido para incluir mais funcionalidades, como relatórios detalhados, exportação de dados, ou integração com outros sistemas.

Para qualquer dúvida ou sugestão, sinta-se à vontade para entrar em contato!
