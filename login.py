import tkinter as tk
import customtkinter as cTk
from urllib.request import urlopen
from PIL import Image
import sqlite3 as sqlite3
import subprocess

cTk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
cTk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(cTk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Džo baidens login peidž")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1), weight=1)
        
        self.appnameframe = cTk.CTkFrame(self)
        self.appnameframe.grid(row=0, column=0, sticky="nsew", columnspan=2, padx=15, pady=10, ipadx=15, ipady=15)
        self.appnameframe.grid_rowconfigure(0, weight=1)
        self.appnameframe.grid_columnconfigure(0, weight=1)

        self.appnamelabel=cTk.CTkLabel(self.appnameframe, text="CSidp")
        self.appnamelabel.grid(row=0, column=0)

        self.loginfieldframe = cTk.CTkFrame(self)
        self.loginfieldframe.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=15, pady=10, ipadx=15, ipady=15)

        self.loginusernamebox=cTk.CTkEntry(self.loginfieldframe, justify=tk.CENTER, placeholder_text="Lietotājvārds")
        self.loginpasswordbox=cTk.CTkEntry(self.loginfieldframe, justify=tk.CENTER, placeholder_text="Parole")
        self.loginbutton=cTk.CTkButton(self.loginfieldframe, text="Ienākt")
        self.registrationbutton=cTk.CTkButton(self.loginfieldframe, text="Reģistrēties", command=self.registrationlauncher)
        self.loginusernamebox.grid(row=0, column=0)
        self.loginpasswordbox.grid(row=0, column=1)
        self.loginbutton.grid(row=1, column=0)
        self.registrationbutton.grid(row=2, column=0)

    def registrationlauncher(self):
       subprocess.run(["python", "registration.py"])





if __name__ == "__main__":
    app = App()
    app.mainloop()