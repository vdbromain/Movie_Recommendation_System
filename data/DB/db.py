# Import to connect to a Postgres DB with python
import psycopg2
import os
import pandas as pd

def connect_db():
    """
    Connecting the postgres DB created on Render.com
    """
    # Connect to the Postgres DB created on Render
    conn = psycopg2.connect(dbname="postgres", user="user", password="password", host="0.0.0.0", port="5432")
    
    # Create the cursor to execute somme querries on the db
    cursor = conn.cursor()
    return conn, cursor

def creating_tables():
    """ 
    create tables in the PostgreSQL database
    """

    # Queries to create the 2 tables called movies & ratings
    queries = (    
    """
    CREATE TABLE movies
    (
        movieId INTEGER NOT NULL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        genre VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE ratings
    (
        userId INTEGER NOT NULL,
        movieId INTEGER NOT NULL,
        rating FLOAT NOT NULL,
        timestamp INTEGER NOT NULL
    )
    """)

    conn = None
    try:
        # Connection to the postgres DB which is on Render.com  
        #conn = psycopg2.connect(database="dragonyte_db", user="dragonyte_db_user", password="iXz2wbLP4YYyV5wt9zGtcu9cYpuEFBtA", host="dpg-cgh9b6t269v15eki92a0-a.frankfurt-postgres.render.com", port="5432")
        #cursor = conn.cursor()
        conn, cursor = connect_db()
        # create table one by one
        for query in queries:
            # Execute the query using the cursor object
            cursor.execute(query)
        # close communication with the PostgreSQL database server
        cursor.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def printing_tables_columns_names():
    conn, cursor = connect_db()

    # Creating a cursor object using the cursor() method
    table_with_column = {}
    tables = ('ratings', 'movies')
    for table in tables:
        #Collect all the columns name of a table and print them
        sql = f'''SELECT * FROM {table}'''
        cursor.execute(sql)
        column_names = [desc[0] for desc in cursor.description]
        table_with_column[table]=column_names
        print(f"For the table named : {table} : {table_with_column[table]}")
        #for i in column_names:
        #    print(i)
        #Put the columns'names in a dict table_name : [columns_name]
    return table_with_column    
    
def deleting_all_the_tables():
    conn, cursor = connect_db()
    # All the table's names  
    tables = ('movies', 'ratings')

    for table in tables :
        # drop table accounts
        query = f'''DROP table IF EXISTS {table}'''
        # Executing the query
        cursor.execute(query)
        print(f"Table {table} dropped !")
    # Commit your changes in the database
    conn.commit()
    # Closing the connection
    conn.close()

def cleaning_csv(file_name="movies.csv"):
    with(open(file_name, "r")) as f :
        next(f)
        print(f[10])


def insert_csv (file_name="movies.csv", table_name="movies"):
    with open(file_name, 'r') as f:
        next(f)  # skip the header row
        conn, cursor = connect_db()
        try:
            cursor.copy_from(f, table_name, sep=',')
        except:
            print("The line has a error")
        finally:
            return print(f"Insert is done for {file_name}")
        
def select_all_data(table_name="movies"):
    conn, cursor = connect_db()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    print(cursor.fetchall())
    

if __name__ == "__main__":
    # Deleting all the tables
    #deleting_all_the_tables()    
    # Create the tables
    #creating_tables()
    # Printing columns'names
    #table_with_column = printing_tables_columns_names()
    #insert_csv()
    #select_all_data()

    cleaning_csv()
    