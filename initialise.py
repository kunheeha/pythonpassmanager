from database import create_connection, create_table

database = r'mypasswords.db'

create_user = '''
CREATE TABLE 'User' (
'id' INTEGER NOT NULL PRIMARY KEY,
'registered' INTEGER NOT NULL  DEFAULT 0,
'name' TEXT DEFAULT 'NULL',
'masterpass' TEXT DEFAULT 'NULL',
'cryptkey' NONE DEFAULT NULL
);'''

create_account_table = '''
CREATE TABLE 'Account' (
'id' INTEGER NOT NULL PRIMARY KEY,
'name' TEXT NOT NULL,
'multiple' INTEGER NOT NULL  DEFAULT 0
);'''

create_password_table = '''
CREATE TABLE 'Password' (
'id' INTEGER NOT NULL PRIMARY KEY,
'prompt' TEXT DEFAULT NULL,
'password' NONE NOT NULL ,
'id_Account' TEXT DEFAULT NULL REFERENCES 'Account' ('id')
);'''

def initialise_db():

    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn, create_user)
        create_table(conn, create_account_table)
        create_table(conn, create_password_table)
        print('Tables successfully created')
        return True
    else:
        print('Error, unable to create connection to db')
        return False
