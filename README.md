
# Password Manager

![](https://onlineworkspace.org/uploadfiles/folder_11/Startscreen.png)

![](https://onlineworkspace.org/uploadfiles/folder_11/useScreen.png)

A completely offline password manager that encrypts passwords and stores them in a database on your local machine.

- GUI - Tkinter (used tkinter to learn it)
- Database - SQLite (used sqlite since it doesn't require server and is self-contained)
- Password encryption - cryptography.fernet
- Master password hashing - SHA-256



## Features

Accounts that have multiple associated passwords 
(for example, bank accounts with digital security password, phone banking password, memorable word, online banking password etc) 
can be created to store each of the different passwords alongside their relevant password prompts in a single 'account' instance 
as well as just generic accounts with a single associated password.



  
## Installation

[Installation Guide](https://www.kunheeha.com/static/Password%20Manager%20%28python%29/Password%20Manager%20%28python%29_installguide.pdf)

### Mac
[Download](https://www.kunheeha.com/software/1) or download the app file from releases

Grant execution permission to passwordmanager script in the app
```bash
  chmod +x [dir to app]/passwordmanager.app/Contents/MacOS/passwordmanager
```

Double click the app and a warning sign will pop up saying that it is from an unidentified developer

Click Open Anyway or open System Preferences -> Security and Privacy -> general and click Allow

Please see [Installation Guide](https://www.kunheeha.com/static/Password%20Manager%20%28python%29/Password%20Manager%20%28python%29_installguide.pdf)
if you run into any errors and the reasons for the steps above 

### Windows
[Download](https://www.kunheeha.com/software/1) or download the exe file from releases

The installer will allow you to specify the installation location and will install a folder called passwordmanager

In the installed folder there is another folder with the same name (passwordmanager) - you can delete everything else

Double click the application file (named passwordmanager) inside the above folder to launch
    
## Roadmap

- All navigation and revealing of passwords to happen in a single window instead of new windows for each of the accounts and passwords.


  