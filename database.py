from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet
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

def add_to_db(connection, sql_statement):
    c = connection.cursor()
    c.execute(sql_statement)
    connection.commit()

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

def login(connection, inputpassword):
    c = connection.cursor()
    c.execute("SELECT masterpass FROM User LIMIT 1;")
    result = c.fetchall()
    match = result[0][0]
    return sha256_crypt.verify(inputpassword, match)
    

def save_account(connection, account_item):
    new_account = (account_item.name, account_item.multiple)
    sql = '''
    INSERT INTO Account(name, multiple)
    VALUES(?,?)
    '''
    c = connection.cursor()
    c.execute(sql, new_account)
    connection.commit()

def save_password(connection, password_item):
    c = connection.cursor()
    c.execute('SELECT cryptkey FROM User LIMIT 1;')
    cryptkey = c.fetchall()[0][0]
    cipher_suite = Fernet(cryptkey)
    password = password_item.password.encode('utf-8')
    new_password = (password_item.prompt, cipher_suite.encrypt(password), password_item.account)
    sql = '''
    INSERT INTO Password(prompt,password,id_Account)
    VALUES(?,?,?)
    '''
    c.execute(sql, new_password)
    connection.commit()


def get_accounts(connection):
    c = connection.cursor()
    c.execute('SELECT id, name FROM Account;')
    return c.fetchall()

def get_passwords(connection, account_id):
    c = connection.cursor()
    c.execute(f'SELECT name, multiple FROM Account WHERE id = {account_id};')
    retrieved_account = c.fetchall()
    account_name = retrieved_account[0][0]
    multiple = retrieved_account[0][1]
    passwords = None
    c.execute(f'SELECT prompt, password FROM Password WHERE id_Account = {account_id}') 
    
    if multiple > 0:
        passwords = c.fetchall()
    else:
        try:
            passwords = c.fetchall()[0][0]
        except:
            pass

    account_info = {
                'multiple': multiple,
                'account_name': account_name,
                'passwords': passwords
            }

    return account_info 
            
def delete_account_db(connection, account_id):
    c = connection.cursor()
    try:
        c.execute(f'DELETE FROM Password WHERE id_Account = {account_id}')
        c.execute(f'DELETE FROM Account WHERE id = {account_id}')
        return True
    except:
        return False





