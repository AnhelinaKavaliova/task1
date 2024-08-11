# Task1 Python introduction

## Description

This project is designed to manage a student and room database using MySQL (or another relational database like PostgreSQL). The main goal is to load data from provided JSON files into the database and perform specific queries to analyze the data

### Problem Statement

Using MySQL, create a data schema that corresponds to the provided files (many-to-one relationship). Write a script to load these files and insert the data into the database

#### Required Queries

1. **List of rooms and the number of students in each room**
2. **Top 5 rooms with the smallest average student age**
3. **Top 5 rooms with the largest age gap among students**
4. **List of rooms with students of different genders**

### Requirements and Notes

- **Optimization**: Propose query optimization options using indexes
- **SQL Query Generation**: Generate SQL queries to add necessary indexes
- **Data Export**: Export results in JSON or XML format
- **Database Operations**: Perform all calculations at the database level
- **Command Line Interface**: The script should support the following input parameters:
  - `students` (path to the students file)
  - `rooms` (path to the rooms file)
  - `format` (output format: XML or JSON)

The script should be written using Object-Oriented Programming (OOP) and adhere to SOLID principles, avoiding the use of ORM (use SQL directly)

## Installation

### Requirements

- Docker
- Python 
- MySQL

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AnhelinaKavaliova/task1.git
    cd task1
    ```

2. **Create a `.env` file in the project root with the following variables:**

    ```plaintext
    HOST=your_mysql_host
    USER=your_mysql_user
    PASSWORD=your_mysql_password
    DATABASE=your_mysql_database
    ```

3. **Start the containers using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

## Usage

1. **Run the Python application using the following command:**

    ```bash
    python src/main.py data/students.json data/rooms.json --format json --output_name output
    ```

2. **Logs of the program will be saved in `py_log.log`.**

## Project Files

- `Dockerfile`: Configuration for building the Python image
- `docker-compose.yml`: Docker Compose configuration to run the application and database
- `mysql-init/`: Scripts for initializing the MySQL database
- `src/`: Source code of the Python application
- `data/`: Data files to be loaded into the database
- `requirements.txt`: Python project dependencies
