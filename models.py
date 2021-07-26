from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet

class User:
    def __init__(self, name, masterpassword):
        self.name = name
        self.key = Fernet.generate_key()
        self.masterpassword = sha256_crypt.encrypt(masterpassword)

class Account:
    def __init__(self, name, multiple):
        self.name = name
        self.multiple = multiple

class Password:
    def __init__(self, password, account):
        self.password = password
        self.account = account
        self.prompt = None
