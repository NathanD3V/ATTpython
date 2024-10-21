# ATTpython
 
SQL: Criar a tabela

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

-- Inserir dados para exemplo
INSERT INTO tb_usuarios (username, senha, role) VALUES ('admin', '12345', 'admin');
INSERT INTO tb_usuarios (username, senha, role) VALUES ('user1', '12345', 'user');

-- baixar o mysql connector 

pip install mysql-connector-python

-- biblioteca do futuro grafico 

pip install matplotlib