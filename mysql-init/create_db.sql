CREATE DATABASE IF NOT EXISTS task1;
USE task1;

CREATE TABLE IF NOT EXISTS rooms (
	id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
	id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    room INT,
    sex CHAR(1),
    FOREIGN KEY (room) REFERENCES rooms(id)
);
