CREATE DATABASE sistema_admin;

USE sistema_admin;

CREATE TABLE administradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO administradores (usuario, senha)
VALUES ('admin', 'Admin@123');
