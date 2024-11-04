#call file name and import function from file connection.py
from connection import create_connection, close_connection
from mysql.connector import Error, errorcode
import pandas as pd

#function create table
def create_table(connection, create_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("Table created successfull")
    except Error as e:
        if e.errno == errorcode.ER_CANT_CREATE_TABLE:
            print(f"The error '{e}' occured")
    finally:
        cursor.close()

def load_csv_to_mysql(connection, table_name, csv_file_path, selected_columns):
    # Read the CSV file into a Dataframe
    df = pd.read_csv(csv_file_path, usecols=selected_columns)
    #print(df.head())
    #print(df.columns)
    #print(df.dtypes)
    
    # prepare the INSERT statement
    cols = ", ".join([f"`{col}`" for col in selected_columns])
    placeholders = ", ".join(["%s"] * len(selected_columns))
    insert_query = f"INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders})"
    
    # Insert data in bulk
    cursor = connection.cursor()
    try:
        cursor.executemany(insert_query, df.values.tolist())
        connection.commit()
        print(f"Data loaded successfully into {table_name}")
    except Exception as e:
        print(f"Error: '{e}' occurred while loading data")
    finally:
        cursor.close()
        
# Main script
if __name__ == "__main__":
    # Connect to the MYSQL database
    connection = create_connection("localhost", "root", "admin!@#$", "book_store")
    
    # Call the function to load CSV data into the table
    csv_file_path = "books.csv" #Replace with your csv file path
    table_name = "books" # Replace with your target table name
    
    # Specify to selected column you want to load 
    selected_columns = ["Title", "Price", "Star", "Stock"] # Replace with your actual column names
     
# Query sql to create table
create_table_query = """CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY, 
    title VARCHAR(255), 
    price FLOAT, 
    star VARCHAR(10), 
    stock VARCHAR(255)) ENGINE = InnoDB"""
    
# Open connection and call function
if connection:
    create_table(connection, create_table_query)
    load_csv_to_mysql(connection, table_name, csv_file_path, selected_columns)
    
#close connection
close_connection