#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connect to MySQL server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password"  # replace with your password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_mysql_password",  # replace with your password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    TABLES = {}
    TABLES['user_data'] = (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "  user_id CHAR(36) PRIMARY KEY,"
        "  name VARCHAR(255) NOT NULL,"
        "  email VARCHAR(255) NOT NULL,"
        "  age DECIMAL(5,2) NOT NULL,"
        "  INDEX(user_id)"
        ") ENGINE=InnoDB"
    )

    cursor = connection.cursor()
    try:
        cursor.execute(TABLES['user_data'])
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    cursor.close()


def insert_data(connection, csv_file):
    """Insert user data from CSV file if not already in database."""
    cursor = connection.cursor()

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
            cursor.execute(query, (row['email'],))
            exists = cursor.fetchone()[0]

            if not exists:
                insert_query = (
                    "INSERT INTO user_data (user_id, name, email, age) "
                    "VALUES (%s, %s, %s, %s)"
                )
                values = (user_id, row['name'], row['email'], float(row['age']))
                cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()
    print("Data inserted successfully")
