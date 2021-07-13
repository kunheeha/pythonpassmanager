import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn
    
def create_table(connection, sql_statement):
    try:
        c = connection.cursor()
        c.execute(sql_statement)

    except Error as e:
        print(e)

def init_user(connection):
    sql = '''
    INSERT INTO User DEFAULT VALUES;
    '''

    try:
        c = connection.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def register_user(connection, user):
    new_user = (user.name, user.masterpassword, user.key)
    sql = '''
    INSERT INTO user(
    '''
    #name
    #masterpass
    #cryptkey



