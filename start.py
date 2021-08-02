import os.path
import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
from database import check_user, create_connection, register_user, login, save_account, get_accounts, get_passwords, delete_account_db, save_password_multiple, save_password_single, get_show_password, delete_pass_db, get_user_name, get_account_name
from initialise import initialise_db
from models import User, Account, Password

# check if database exists, if not create mypasswords.db 
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

        tk.Tk.geometry(self, "600x250")
        # Placing window on centre of screen
        # adapted from https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        positionRight = int(self.winfo_screenwidth()/2 - 600/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        tk.Tk.geometry(self, f'+{positionRight}+{positionDown}')
        
        # set icon
        icon = tk.PhotoImage(file='lock_icon.png')
        tk.Tk.iconphoto(self, False, icon)
        # set title of window
        tk.Tk.wm_title(self, 'Password Manager')

        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RegisterPage, LoginPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        global MainScreen_obj
        MainScreen_obj = MainScreen(container, self)
        self.frames[MainScreen] = MainScreen_obj
        MainScreen_obj.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# if user exists, show option to enter login page
# if user doesn't exist, show option to enter register page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        if usercheck:
            start_frame = tk.LabelFrame(self, text='Enter Password Manager', padx=180, pady=50)
        else:
            start_frame = tk.LabelFrame(self, text='Welcome to your Password Manager', padx=180, pady=50)
            
        start_frame.pack(padx=25, pady=25)
        register_button = ttk.Button(start_frame, text="Start", command=lambda: controller.show_frame(RegisterPage))
        login_button = ttk.Button(start_frame, text="Login", command=lambda: controller.show_frame(LoginPage))
        if usercheck:
            login_button.pack()
        else:
            register_button.pack()

        mydetails = tk.Label(self, text='created by Kunhee Ha\nsource code: https://github.com/kunheeha/pythonpassmanager')
        mydetails.pack()

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_var = tk.StringVar()
        self.passw_var = tk.StringVar()
        
        register_frame = tk.LabelFrame(self, text='Register', padx=180, pady=10)
        register_frame.pack(padx=25, pady=25)
        prompt_label = tk.Label(register_frame, text='Enter details below')
        name_label = tk.Label(register_frame, text='Name')
        passw_label = tk.Label(register_frame, text='Master Password')
        
        name_entry = tk.Entry(register_frame, textvariable=self.name_var)
        passw_entry = tk.Entry(register_frame, show='*', textvariable=self.passw_var)

        prompt_label.pack()
        name_label.pack()
        name_entry.pack()
        passw_label.pack()
        passw_entry.pack()
        # add register function
        register_user_button = ttk.Button(register_frame, text='Register', command=lambda: self.register(self.controller))
        register_user_button.pack()

    def register(self, controller):
        name = self.name_var.get()
        passw = self.passw_var.get()
        new_user = User(name, passw)
        register_user(conn, new_user)
        
        # adding example account and password to db before user logs in for first time
        example_account = Account('Example', 1)
        example_password = Password('my$uperS3cretP@assword', 1)
        example_password.prompt = 'This is an example password'

        save_account(conn, example_account)
        save_password_multiple(conn, example_password)
        MainScreen_obj.refresh()

        controller.show_frame(LoginPage)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.passw_var = tk.StringVar()

        login_frame = tk.LabelFrame(self, text='Login', padx=180, pady=45)
        login_frame.pack(padx=25, pady=25)

        prompt_label = tk.Label(login_frame, text='Enter Master Password')
        passw_entry = tk.Entry(login_frame, show='*', textvariable=self.passw_var)
        login_button = ttk.Button(login_frame, text='Login', command=lambda: self.login_attempt(self.controller))
        self.fail_label = tk.Label(login_frame, text='Login Failed, try again')

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
        top_frame = tk.LabelFrame(self, text='Password Manager', padx=10, pady=10)
        top_frame.pack(padx=25, pady=25)
        welcome_label = tk.Label(top_frame, text=f'Welcome {get_user_name(conn)}')
        welcome_label.grid(row=0, column=0, padx=(10, 100))
        add_account_button = ttk.Button(top_frame, text='New Account', command=lambda: self.add_new_account(self.controller))
        add_account_button.grid(row=0, column=1, padx=(100, 10))

        self.accounts = get_accounts(conn)
        self.shown_accounts = {}

        self.accounts_frame = tk.LabelFrame(self, text='Your Accounts', padx=10, pady=10)
        self.accounts_frame.pack(padx=25, pady=10)
        
        self.col_number = 0
        self.row_number = 0
        # retrieve all existing accounts and store them in self.shown_accounts
        for x in range(len(self.accounts)):
            i = self.accounts[x][0]
            self.shown_accounts[f'account_{x}'] = ttk.Button(self.accounts_frame, text=self.accounts[x][1], command=lambda i=i: self.view_account(i))
            self.shown_accounts[f'account_{x}'].grid(row=self.row_number, column=self.col_number)
            if self.col_number >= 5:
                self.col_number = 0
                self.row_number += 1
            else:
                self.col_number += 1

    def refresh(self):
        # reset col and row numbers
        self.col_number = 0
        self.row_number = 0
        self.accounts = get_accounts(conn)
        for w in self.shown_accounts:
            self.shown_accounts[w].destroy()
        self.shown_accounts = {}
        
        # retrieve all existing accounts and store them in self.shown_accounts
        for x in range(len(self.accounts)):
            i = self.accounts[x][0]
            self.shown_accounts[f'account_{x}'] = ttk.Button(self.accounts_frame, text=self.accounts[x][1], command=lambda i=i: self.view_account(i))
            self.shown_accounts[f'account_{x}'].grid(row=self.row_number, column=self.col_number)
            if self.col_number >= 5:
                self.col_number = 0
                self.row_number += 1
            else:
                self.col_number += 1

    # create new screen to show passwords in specified account
    # doesn't display the actual passwords unless prompted by button on this screen
    def view_account(self, account_id):
        AccountPage = tk.Toplevel()
        this_account = get_passwords(conn, account_id)
        AccountPage.title(this_account['account_name'])
        AccountPage.geometry("300x250")
        # Placing window on centre of screen
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        AccountPage.geometry(f'+{positionRight}+{positionDown}')

        account_frame = tk.LabelFrame(AccountPage, text=f'Account: {this_account["account_name"]}', padx=10, pady=10)
        account_frame.pack()

        # multiple passwords with existing passwords in db
        # show password prompts and add_pass button
        if this_account['multiple'] > 0 and len(this_account['passwords']) > 0:
            prompt_frame = tk.LabelFrame(account_frame, text='Password prompts', padx=10, pady=10)
            prompt_frame.pack()
            col_number = 0
            row_number = 0
            shown_passwords = {}
            for x in range(len(this_account['passwords'])):
                i = this_account['passwords'][x][1]
                shown_passwords[f'pass_{x}'] = ttk.Button(prompt_frame, text=this_account['passwords'][x][0], command=lambda i=i: self.show_password(i, account_id, AccountPage))
                shown_passwords[f'pass_{x}'].grid(row=row_number, column=col_number)
                if col_number >= 1:
                    col_number = 0
                    row_number += 1
                else:
                    col_number += 1

            add_pass_button = ttk.Button(account_frame, text='Add Password', command=lambda: self.add_password_screen(AccountPage, True, account_id))
            add_pass_button.pack()

        # multiple passwords and no existing passwords in db
        # show add_pass button
        elif this_account['multiple'] > 0 and len(this_account['passwords']) == 0:
            add_pass_button = ttk.Button(account_frame, text='Add Password', command=lambda: self.add_password_screen(AccountPage, True, account_id))
            add_pass_button.pack()

        # single password for account existing in db
        elif not this_account['passwords'] is None:
            show_pass_button = ttk.Button(account_frame, text='Show Password', command=lambda: self.show_password(this_account['passwords'][1], account_id, AccountPage))
            show_pass_button.pack()

        # single password but no existing password in db
        # show add_pass button
        elif this_account['passwords'] is None:    
            add_pass_button = ttk.Button(account_frame, text='Add Password', command=lambda: self.add_password_screen(AccountPage, False, account_id))
            add_pass_button.pack()

        delete_account_button = ttk.Button(AccountPage, text='Delete Account', command=lambda: self.delete_account_confirm(account_id, AccountPage))
        delete_account_button.pack()

    # create new screen with password and delete button
    def show_password(self, pass_id, account_id, accountScreen):
        PasswordScreen = tk.Toplevel()
        PasswordScreen.geometry("300x250")
        # Placing window on centre of screen
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        PasswordScreen.geometry(f'+{positionRight}+{positionDown}')

        password = get_show_password(conn, pass_id).decode('utf-8')
        pass_label = tk.Label(PasswordScreen, text=password)
        delete_pass_button = ttk.Button(PasswordScreen, text='Delete Password', command=lambda: self.delete_password_confirm(pass_id, PasswordScreen, accountScreen, account_id))
        
        pass_label.pack()
        delete_pass_button.pack()

    # create new screen to confirm password delete
    def delete_password_confirm(self, pass_id, parentScreen, accountScreen, account_id):
        ConfirmDelPass = tk.Toplevel()
        ConfirmDelPass.geometry("300x250")
        # Placing window on centre of screen
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        ConfirmDelPass.geometry(f'+{positionRight}+{positionDown}')

        this_pass = get_show_password(conn, pass_id).decode('utf-8')
        confirm_label = tk.Label(ConfirmDelPass, text=f'Are you sure you want to delete password: {this_pass}?')
        confirm_button = ttk.Button(ConfirmDelPass, text='Delete', command=lambda: self.delete_password(pass_id, ConfirmDelPass, parentScreen, accountScreen, account_id))

        confirm_label.pack()
        confirm_button.pack()

    # deleting password destorys del_pass_confirm screen and show_pass screen
    def delete_password(self, pass_id, currentScreen, parentScreen, accountScreen, account_id):
        if delete_pass_db(conn, pass_id) is True:
            currentScreen.destroy()
            parentScreen.destroy()
            accountScreen.destroy()
            self.view_account(account_id)

        else:
            print('error')

    # create new screen with password_var to take input
    def add_password_screen(self, account_screen, multiple, account_id):
        AddPasswordScreen = tk.Toplevel()
        AddPasswordScreen.geometry("300x250")
        # Placing window on centre of screen
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        AddPasswordScreen.geometry(f'+{positionRight}+{positionDown}')

        password_var = tk.StringVar()
        password_label = tk.Label(AddPasswordScreen, text='Password')
        password_entry = tk.Entry(AddPasswordScreen, textvariable=password_var)
        # account has multiple associated passwords 
        if multiple:
            prompt_var = tk.StringVar()
            prompt_label = tk.Label(AddPasswordScreen, text='Password Prompt')
            prompt_entry = tk.Entry(AddPasswordScreen, textvariable=prompt_var)
            add_password_button = ttk.Button(AddPasswordScreen, text='Add', command=lambda: self.add_password(account_screen, AddPasswordScreen, multiple, account_id, prompt=prompt_var.get(), password=password_var.get()))

            prompt_label.pack()
            prompt_entry.pack()
            password_label.pack()
            password_entry.pack()
            add_password_button.pack()
        # account only has one associated password
        elif not multiple:
            add_password_button = ttk.Button(AddPasswordScreen, text='Add', command=lambda: self.add_password(account_screen, AddPasswordScreen, multiple, account_id, password=password_var.get()))
            password_label.pack()
            password_entry.pack()
            add_password_button.pack()

           
    # collect user input from add_pass_screen to add to database
    def add_password(self, accountScreen, currentScreen,  multiple, account_id, **kwargs):
        if multiple:
            new_password = Password(kwargs['password'], account_id)
            new_password.prompt = kwargs['prompt']
            save_password_multiple(conn, new_password)
        elif not multiple:
            new_password = Password(kwargs['password'], account_id)
            save_password_single(conn, new_password)

        accountScreen.destroy()
        currentScreen.destroy()
        self.view_account(account_id)


    # create new screen to confirm deletion of specified account and all its associated passwords
    def delete_account_confirm(self, account_id, parentScreen):
        ConfirmDelete = tk.Toplevel()
        ConfirmDelete.geometry("300x250")
        # Placing window on centre of screen
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        ConfirmDelete.geometry(f'+{positionRight}+{positionDown}')

        this_account = get_passwords(conn, account_id)
        confirm_label = tk.Label(ConfirmDelete, text=f'Are you sure you want to delete {this_account["account_name"]}?')
        confirm_button = ttk.Button(ConfirmDelete, text='Delete', command=lambda: self.delete_account(account_id, ConfirmDelete, parentScreen))

        confirm_label.pack()
        confirm_button.pack()

    # deletes account and associated passwords
    # destroys del_acc_screen and account info screen
    def delete_account(self, account_id, currentScreen, parentScreen):
        if delete_account_db(conn, account_id) is True:
            self.refresh()
            currentScreen.destroy()
            parentScreen.destroy()

        else:
            print('error')

    # create new screen to take input about new account entry
    def add_new_account(self, controller):
        #controller.show_frame(AddAccount)
        AddAccount = tk.Toplevel(self)
        AddAccount.geometry("300x250")
        # Placing window on centre of screen
        positionRight = int(self.winfo_screenwidth()/2 - 300/2)
        positionDown = int(self.winfo_screenheight()/2 - 250/2)
        AddAccount.geometry(f'+{positionRight}+{positionDown}')


        self.account_name_var = tk.StringVar()
        self.multiple_passwords_var = tk.IntVar()

        account_name_label = tk.Label(AddAccount, text='Account Name')
        multiple_passwords = tk.Checkbutton(AddAccount, text='Check if this account has multiple passwords', variable=self.multiple_passwords_var, onvalue=1, offvalue=0)
        account_name_entry = tk.Entry(AddAccount, textvariable=self.account_name_var)
        add_button = ttk.Button(AddAccount, text='Add', command=lambda: self.add_account(AddAccount))

        account_name_label.pack()
        account_name_entry.pack()
        multiple_passwords.pack()
        add_button.pack()


    # adds new account to database and destorys current screen
    # refreshes the accounts shown on main screen by deleting all button on self.shown_accounts
    def add_account(self, currentScreen):
        account_name = self.account_name_var.get()
        multiple_passwords = self.multiple_passwords_var.get()
        new_account = Account(account_name, multiple_passwords)
        save_account(conn, new_account)

        self.refresh()
        currentScreen.destroy()







app = PassManagerApp()
app.mainloop()


