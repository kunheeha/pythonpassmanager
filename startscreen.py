import os.path
import tkinter as tk
from database import check_user, create_connection, register_user, login
from initialise import initialise_db
from models import User


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

        for F in (StartPage, RegisterPage, LoginPage, SuccessTest):

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

        prompt_label.pack()
        passw_entry.pack()
        login_button.pack()
        
    def login_attempt(self, controller):
        passw = self.passw_var.get()
        if login(conn, passw):
            controller.show_frame(SuccessTest)
        else:
            print('login failed')

class SuccessTest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        prompt_label = tk.Label(self, text='Success!')
        prompt_label.pack()

app = PassManagerApp()
app.mainloop()

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


#def register_screen():
#    global name_var
#    global passw_var
#    name_var = StringVar()
#    passw_var = StringVar()
#    
#    register_button.pack_forget()
#    root.title('Register')
#    prompt_label = tk.Label(root, text='Enter details below').pack()
#    name_label = tk.Label(root, text='Name').pack()
#    name_entry = Entry(root, textvariable=name_var)
#    pass_entry = Entry(root, textvariable=passw_var)
#    name_entry.pack()
#    pass_label = tk.Label(root, text='Master Password').pack()
#    pass_entry.pack()
#    register_user_button = Button(root, text='Register', command=register)
#    register_user_button.pack()



