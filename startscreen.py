import os.path
import tkinter as tk
from cryptography.fernet import Fernet
from database import check_user, create_connection, register_user, login, save_account, get_accounts, get_passwords, delete_account_db, save_password_multiple, save_password_single, get_show_password, delete_pass_db
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
        self.shown_accounts = {}

        for x in range(len(self.accounts)):
            i = self.accounts[x][0]
            self.shown_accounts[f'account_{x}'] = tk.Button(self, text=self.accounts[x][1], command=lambda i=i: self.view_account(i))
            self.shown_accounts[f'account_{x}'].pack()

        add_account_button = tk.Button(self, text='New Account', command=lambda: self.add_new_account(self.controller))
        add_account_button.pack()

    def show_password(self, pass_id):
        PasswordScreen = tk.Toplevel()
        password = str(get_show_password(conn, pass_id))
        pass_label = tk.Label(PasswordScreen, text=password)
        delete_pass_button = tk.Button(PasswordScreen, text='Delete Password', command=lambda: self.delete_password_confirm(pass_id, PasswordScreen))
        
        pass_label.pack()
        delete_pass_button.pack()

    def delete_password_confirm(self, pass_id, parentScreen):
        ConfirmDelPass = tk.Toplevel()
        this_pass = str(get_show_password(conn, pass_id))
        confirm_label = tk.Label(ConfirmDelPass, text=f'Are you sure you want to delete password: {this_pass}?')
        confirm_button = tk.Button(ConfirmDelPass, text='Delete', command=lambda: self.delete_password(pass_id, ConfirmDelPass, parentScreen))

        confirm_label.pack()
        confirm_button.pack()

    def delete_password(self, pass_id, currentScreen, parentScreen):
        if delete_pass_db(conn, pass_id) is True:
            currentScreen.destroy()
            parentScreen.destroy()

        else:
            print('error')

    def add_password_screen(self, multiple, account_id):
        AddPasswordScreen = tk.Toplevel()
        password_var = tk.StringVar()
        password_label = tk.Label(AddPasswordScreen, text='Password')
        password_entry = tk.Entry(AddPasswordScreen, textvariable=password_var)
        if multiple:
            prompt_var = tk.StringVar()
            prompt_label = tk.Label(AddPasswordScreen, text='Password Prompt')
            prompt_entry = tk.Entry(AddPasswordScreen, textvariable=prompt_var)
            add_password_button = tk.Button(AddPasswordScreen, text='Add', command=lambda: self.add_password(multiple, account_id, prompt=prompt_var.get(), password=password_var.get()))

            prompt_label.pack()
            prompt_entry.pack()
            password_label.pack()
            password_entry.pack()
            add_password_button.pack()
        elif not multiple:
            add_password_button = tk.Button(AddPasswordScreen, text='Add', command=lambda: self.add_password(multiple, account_id, password=password_var.get()))
            password_label.pack()
            password_entry.pack()
            add_password_button.pack()

           
    def add_password(self, multiple, account_id, **kwargs):
        if multiple:
            new_password = Password(kwargs['password'], account_id)
            new_password.prompt = kwargs['prompt']
            save_password_multiple(conn, new_password)
        elif not multiple:
            new_password = Password(kwargs['password'], account_id)
            save_password_single(conn, new_password)

    def view_account(self, account_id):
        AccountPage = tk.Toplevel()
        this_account = get_passwords(conn, account_id)

        print(this_account)

        # multiple passwords with existing passwords in db
        # show password prompts and add_pass button
        if this_account['multiple'] > 0 and len(this_account['passwords']) > 0:
            shown_passwords = {}
            for x in range(len(this_account['passwords'])):
                i = this_account['passwords'][x][1]
                shown_passwords[f'pass_{x}'] = tk.Button(AccountPage, text=this_account['passwords'][x][0], command=lambda i=i: self.show_password(i))
                shown_passwords[f'pass_{x}'].pack()

            add_pass_button = tk.Button(AccountPage, text='Add Password', command=lambda: self.add_password_screen(True, account_id))
            add_pass_button.pack()

        # multiple passwords and no existing passwords in db
        # show add_pass button
        elif this_account['multiple'] > 0 and len(this_account['passwords']) == 0:
            add_pass_button = tk.Button(AccountPage, text='Add Password', command=lambda: self.add_password_screen(True, account_id))
            add_pass_button.pack()

        # single password for account existing in db
        elif not this_account['passwords'] is None:
            show_pass_button = tk.Button(AccountPage, text='Show Password', command=lambda: self.show_password(this_account['passwords'][1]))
            show_pass_button.pack()

        # single password but no existing password in db
        # show add_pass button
        elif this_account['passwords'] is None:    
            add_pass_button = tk.Button(AccountPage, text='Add Password', command=lambda: self.add_password_screen(False, account_id))
            add_pass_button.pack()

        delete_account_button = tk.Button(AccountPage, text='Delete Account', command=lambda: self.delete_account_confirm(account_id, AccountPage))
        delete_account_button.pack()

    def delete_account_confirm(self, account_id, parentScreen):
        ConfirmDelete = tk.Toplevel()
        this_account = get_passwords(conn, account_id)
        confirm_label = tk.Label(ConfirmDelete, text=f'Are you sure you want to delete {this_account["account_name"]}?')
        confirm_button = tk.Button(ConfirmDelete, text='Delete', command=lambda: self.delete_account(account_id, ConfirmDelete, parentScreen))

        confirm_label.pack()
        confirm_button.pack()

    def delete_account(self, account_id, currentScreen, parentScreen):
        if delete_account_db(conn, account_id) is True:
            self.accounts = get_accounts(conn)
            for w in self.shown_accounts:
                self.shown_accounts[w].destroy()
            self.shown_accounts = {}
            for x in range(len(self.accounts)):
                i = self.accounts[x][0]
                self.shown_accounts[f'account_{x}'] = tk.Button(self, text=self.accounts[x][1], command=lambda i=i: self.view_account(i))
                self.shown_accounts[f'account_{x}'].pack()

                currentScreen.destroy()
                parentScreen.destroy()

        else:
            print('error')
        




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
            self.shown_accounts[w].destroy()
        self.shown_accounts = {}
        for x in range(len(self.accounts)):
            i = self.accounts[x][0]
            self.shown_accounts[f'account_{x}'] = tk.Button(self, text=self.accounts[x][1], command=lambda i=i: self.view_account(i))
            self.shown_accounts[f'account_{x}'].pack()
        
        currentScreen.destroy()







app = PassManagerApp()
app.mainloop()


