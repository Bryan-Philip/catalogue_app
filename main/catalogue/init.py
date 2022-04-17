### Use this program to initialize the database
### Do not use if the database is already initialized as this will reset the database

### Uncomment below to run the initializer program

from mysql.connector import connect, Error
import mysql
from connector import CONNECTOR

database_data = open("catalogue.sql", "r") 
database_init = database_data.read()
database_data.close()

try:
    with connect(**CONNECTOR) as connection:
        print(connection)
        with connection.cursor() as cursor:
            cursor.execute(database_init)
except Error as e:
    print(e)
    
# from contextlib import ContextDecorator

# class my_connect(ContextDecorator):
#     def __init__(self):
#         self.data_base_connection = ''

#     def __enter__(self):
#         self.data_base_connection = mysql.connect(
#         host='localhost',
#         user='winston',
#         passwd='winston',
#         db='catalogue',)
#         cursor = self.data_base_connection.cursor()
#         return cursor

#     def __exit__(self, *exc):
#         self.data_base_connection.close()
#         return False

# def query_tables():
#     with my_connect() as cursor:
#         database_data = open("catalogue.sql", "r") 
#         database_init = database_data.read()
#         database_data.close()
#         try:
#             cursor.execute(database_init)
#         except Error as e:
#             print(e)
            
# query_tables()