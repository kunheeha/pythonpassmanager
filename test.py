from passlib.hash import sha256_crypt
from models import User

# Create testuser and check it's password can be verified with sha256_crypt
def test_user():
    testuser = User('username', 'password')
    assert testuser.name == 'username'
    assert sha256_crypt.verify('password', testuser.masterpassword) == True

if __name__ == '__main__':
    test_user()
    print('all tests have passed')
