from passlib.hash import sha256_crypt
from models import User
from database import check_user, create_connection, register_user

# Check that it connects to database correctly
def database_connection(database_name):
    conn = create_connection(database_name)
    assert conn != None

# Create testuser and check it's password can be verified with sha256_crypt
def test_user():
    testuser = User('username', 'password')
    assert testuser.name == 'username'
    assert sha256_crypt.verify('password', testuser.masterpassword) == True

# Check there is no User at first instance
def check_no_user(database_name):
    conn = create_connection(database_name)
    assert check_user(conn) == []

# Check user is registered
def check_user_registration():
    testuser = User('username', 'password')
    conn = create_connection(r"mypasswords.db")
    print(register_user(conn, testuser))

    


if __name__ == '__main__':
    test_user()
    check_user_registration()
    print('all tests have passed')
