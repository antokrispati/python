import mysql.connector
from mysql.connector import Error

def create_connection(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "admin!@#$",
            database = "book_store"
    )
        print("Connection to MySQL DB Successful")
    except Error as e:
        print(f"The error '{e}' occured")
    
    return connection

    
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("The connection is closed")