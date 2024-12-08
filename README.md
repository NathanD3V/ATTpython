# Requerimentos para o codigo ser executavel além do python
 
MySQL: Criar a tabela/banco de dados

1. Comandos:
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

2. Em seguida inserir dados de registro pelo MySQL

-- Inserir dados para exemplo
INSERT INTO tb_usuarios (username, senha, role) VALUES ('admin', '12345', 'admin');
INSERT INTO tb_usuarios (username, senha, role) VALUES ('user1', '12345', 'user');

3. Baixar as dependencias para se executar:
-- Interface gráfica
pip install tk

-- baixar o mysql connector 
pip install mysql-connector-python

-- biblioteca do grafico 
pip install matplotlib


4. Manter a senha "12345" ou mudar a senha no código para se executar o codigo 
e ter acesso ao banco de dados