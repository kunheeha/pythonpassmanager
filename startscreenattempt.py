import os.path
from tkinter import *
from database import check_user, create_connection, register_user
from initialise import initialise_db
from models import User


root = Tk()
root.title('Password Manager')

# include a popup message window when failing to create databse

database_exists = os.path.exists('mypasswords.db')
if not database_exists:
    successful_init = initialise_db()
    if not successful_init:
        print('failed to create database')

conn = create_connection(r'mypasswords.db')
usercheck = len(check_user(conn)) > 0

#def login_screen():
#    global masterpass_var
#    masterpass_var = StringVar()
#    login_button.pack_forget()
#    close_button.pack_forget()
#    prompt_label.text = 'Enter Master Password'
#    name_label.pack_forget()
#    name_entry.pack_forget()
#    register_user_button.pack_forget()
#    pass_entry.textvariable = masterpass_var
#
#    login_button = Button(root, text='Login')
#    login_button.pack()

def register():
    name = name_var.get()
    passw = passw_var.get()
    new_user = User(name, passw)
    register_user(conn, new_user)
    login_screen()

def register_screen():
    global name_var
    global passw_var
    name_var = StringVar()
    passw_var = StringVar()
    
    register_button.pack_forget()
    root.title('Register')
    prompt_label = Label(root, text='Enter details below').pack()
    name_label = Label(root, text='Name').pack()
    name_entry = Entry(root, textvariable=name_var)
    pass_entry = Entry(root, textvariable=passw_var)
    name_entry.pack()
    pass_label = Label(root, text='Master Password').pack()
    pass_entry.pack()
    register_user_button = Button(root, text='Register', command=register)
    register_user_button.pack()

register_button = Button(root, text="Start", command=register_screen)
login_button = Button(root, text="Login")
close_button = Button(root, text="Close")


def startscreen():
    if usercheck == True:
        login_button.pack()
        close_button.pack()
    else:
        register_button.pack()


startscreen()
root.mainloop()
