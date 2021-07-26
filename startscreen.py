import os.path
import tkinter as tk
from cryptography.fernet import Fernet
from database import check_user, create_connection, register_user, login, save_account, get_accounts, get_passwords
from initialise import initialise_db
from models import User, Account, Password


database_exists = os.path.exists('mypasswords.db')
if not database_exists:
    successful_init = initialise_db()
    if not successful_init:
        print('failed to create database')

conn = create_connection(r'mypasswords.db')
usercheck = len(check_user(conn)) > 0

class PassManagerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RegisterPage, LoginPage, MainScreen):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        register_button = tk.Button(self, text="Start", command=lambda: controller.show_frame(RegisterPage))
        login_button = tk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))
        close_button = tk.Button(self, text="Close")
        if usercheck:
            login_button.pack()
            close_button.pack()
        else:
            register_button.pack()

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_var = tk.StringVar()
        self.passw_var = tk.StringVar()
        
        prompt_label = tk.Label(self, text='Enter details below')
        name_label = tk.Label(self, text='Name')
        passw_label = tk.Label(self, text='Master Password')
        
        name_entry = tk.Entry(self, textvariable=self.name_var)
        passw_entry = tk.Entry(self, textvariable=self.passw_var)

        prompt_label.pack()
        name_label.pack()
        name_entry.pack()
        passw_label.pack()
        passw_entry.pack()
        # add register function
        register_user_button = tk.Button(self, text='Register', command=lambda: self.register(self.controller))
        register_user_button.pack()

    def register(self, controller):
        name = self.name_var.get()
        passw = self.passw_var.get()
        new_user = User(name, passw)
        register_user(conn, new_user)
        controller.show_frame(LoginPage)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.passw_var = tk.StringVar()

        prompt_label = tk.Label(self, text='Enter Master Password')
        passw_entry = tk.Entry(self, textvariable=self.passw_var)
        login_button = tk.Button(self, text='Login', command=lambda: self.login_attempt(self.controller))
        self.fail_label = tk.Label(self, text='Login Failed, try again')

        prompt_label.pack()
        passw_entry.pack()
        login_button.pack()
        
    def login_attempt(self, controller):
        passw = self.passw_var.get()
        if login(conn, passw):
            controller.show_frame(MainScreen)
        else:
            self.fail_label.pack()
            

class MainScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.accounts = get_accounts(conn)
        self.shown_accounts = []
        self.shown_accounts_x = {}

        for x in range(len(self.accounts)):
            i = self.accounts[x][0]
            self.shown_accounts_x[f'account_{x}'] = tk.Button(self, text=self.accounts[x][1], command=lambda i=i: self.view_account(i))
            self.shown_accounts_x[f'account_{x}'].pack()

        print(self.shown_accounts_x)

#        for account in self.accounts:
#            accountbutton = tk.Button(self, text=account[1], command=lambda: self.view_account(account[0]))
#            accountbutton.pack()
#            self.shown_accounts.append(accountbutton)

        add_account_button = tk.Button(self, text='New Account', command=lambda: self.add_new_account(self.controller))
        add_account_button.pack()

    def view_account(self, account_id):
        #AccountPage = tk.Toplevel()
        print(account_id)


    def add_new_account(self, controller):
        #controller.show_frame(AddAccount)
        AddAccount = tk.Toplevel(self)

        self.account_name_var = tk.StringVar()
        self.multiple_passwords_var = tk.IntVar()

        account_name_label = tk.Label(AddAccount, text='Account Name')
        multiple_passwords = tk.Checkbutton(AddAccount, text='Check if this account has multiple passwords', variable=self.multiple_passwords_var, onvalue=1, offvalue=0)
        account_name_entry = tk.Entry(AddAccount, textvariable=self.account_name_var)
        add_button = tk.Button(AddAccount, text='Add', command=lambda: self.add_account(AddAccount))

        account_name_label.pack()
        account_name_entry.pack()
        multiple_passwords.pack()
        add_button.pack()


    def add_account(self, currentScreen):
        account_name = self.account_name_var.get()
        multiple_passwords = self.multiple_passwords_var.get()
        new_account = Account(account_name, multiple_passwords)
        save_account(conn, new_account)

        self.accounts = get_accounts(conn)
        for w in self.shown_accounts:
            w.destroy()
        self.shown_accounts = []
        for account in self.accounts:
            accountbutton = tk.Button(self, text=account[1], command=lambda: self.view_account(account[0]))
            accountbutton.pack()
            self.shown_accounts.append(accountbutton)
        
        currentScreen.destroy()







app = PassManagerApp()
app.mainloop()


