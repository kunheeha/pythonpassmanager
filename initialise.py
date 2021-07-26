from database import create_connection, create_table, add_to_db

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

add_example_account = '''
INSERT INTO Account(name, multiple)
VALUES('Example',1)
'''

add_example_password = '''
INSERT INTO Password(prompt, password, id_Account)
VALUES('Enter Password','mypassword',1)
'''

def initialise_db():

    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn, create_user)
        create_table(conn, create_account_table)
        create_table(conn, create_password_table)
        print('Tables successfully created')
        add_to_db(conn, add_example_account)
        add_to_db(conn, add_example_password)
        return True
    else:
        print('Error, unable to create connection to db')
        return False
