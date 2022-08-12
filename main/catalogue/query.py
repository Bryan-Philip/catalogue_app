from mysql.connector import connect, Error
from main.catalogue.connector import CONNECTOR

def DatabaseQueryProducerCompany(mark):
    try:
        with connect(**CONNECTOR) as connection:
            ins = (mark,)
            init_values = "SELECT `company` FROM `producers` WHERE `mark` = %s"
            with connection.cursor() as cursor:
                cursor.execute(init_values, ins)
                rows = cursor.fetchone()
                if(rows != None):
                    return rows[0]
                else:
                    return None
    except Error as e:
        print(e)

def DatabaseQueryProducerAddress(mark):
    try:
        with connect(**CONNECTOR) as connection:
            ins = (mark,)
            init_values = "SELECT `postal_address` FROM `producers` WHERE `mark` = %s"
            with connection.cursor() as cursor:
                cursor.execute(init_values, ins)
                rows = cursor.fetchone()
                if(rows != None):
                    return rows[0]
                else:
                    return None
    except Error as e:
        print(e)

def DatabaseQueryWarehouseCompany(code):
    try:
        with connect(**CONNECTOR) as connection:
            ins = (code,)
            init_values = "SELECT `company` FROM `warehouses` WHERE `code` = %s"
            with connection.cursor() as cursor:
                cursor.execute(init_values, ins)
                rows = cursor.fetchone()
                if(rows != None):
                    return rows[0]
                else:
                    return None
    except Error as e:
        print(e)
        
def DatabaseQueryWarehouseAddress(code):
    try:
        with connect(**CONNECTOR) as connection:
            ins = (code,)
            init_values = "SELECT `postal_address` FROM `warehouses` WHERE `code` = %s"
            with connection.cursor() as cursor:
                cursor.execute(init_values, ins)
                rows = cursor.fetchone()
                if(rows != None):
                    return rows[0]
                else:
                    return None
    except Error as e:
        print(e)
        
def DatabaseQueryBuyerCompany(code):
    try:
        with connect(**CONNECTOR) as connection:
            ins = (code,)
            init_values = "SELECT `company` FROM `buyers` WHERE `code` = %s"
            with connection.cursor() as cursor:
                cursor.execute(init_values, ins)
                rows = cursor.fetchone()
                if(rows != None):
                    return rows[0]
                else:
                    return None
    except Error as e:
        print(e)
        
def DatabaseQueryBuyerAddress(code):
    try:
        with connect(**CONNECTOR) as connection:
            ins = (code,)
            init_values = "SELECT `postal_address` FROM `buyers` WHERE `code` = %s"
            with connection.cursor() as cursor:
                cursor.execute(init_values, ins)
                rows = cursor.fetchone()
                if(rows != None):
                    return rows[0]
                else:
                    return None
    except Error as e:
        print(e)