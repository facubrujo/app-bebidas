-- Crear la base de datos
CREATE DATABASE CocktelesArg;

-- Usar la base de datos
USE CocktelesArg;

-- Crear la tabla usuarios
CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    genero VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    mayor VARCHAR(80) NOT NULL,
    rol VARCHAR(80) NOT NULL,
    alta BOOLEAN, 
    image LONGBLOB,
    PRIMARY KEY (id)
);

select * from usuarios;


