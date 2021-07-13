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


def check_user(connection):
    c = connection.cursor()
    c.execute("SELECT registered FROM User LIMIT 1;")
    result = c.fetchall()
    return result

def register_user(connection, user):
    new_user = (1, user.name, user.masterpassword, user.key)
    sql = '''
    INSERT INTO User(registered,name,masterpass,cryptkey)
    VALUES(?,?,?,?)
    '''
    c = connection.cursor()
    c.execute(sql, new_user)
    connection.commit()
    return c.lastrowid



