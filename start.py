import os.path
from tkinter import *
from database import check_user, create_connection
from initialise import initialise_db

database_exists = os.path.exists('mypasswords.db')
if not database_exists:
    successful_init = initialise_db()
    if not successful_init:
        print('failed to create database')

conn = create_connection(r'mypasswords.db')
usercheck = len(check_user(conn)) > 0

class Start:
    def __init__(self, master, usercheck):
        self.master = master
        master.title("Password Manager")

        self.register_button = Button(master, text="Start")
        self.login_button = Button(master, text="Login")
        self.close_button = Button(master, text="Close")

        if usercheck == True:
            self.login_button.pack()
            self.close_button.pack()
        else:
            self.register_button.pack()

root = Tk()

startGUI = Start(root, usercheck)
root.mainloop()
