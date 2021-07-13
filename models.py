from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet

class User:
    def __init__(self, name, masterpassword):
        self.name = name
        self.key = Fernet.generate_key()
        self.masterpassword = sha256_crypt.encrypt(masterpassword)

