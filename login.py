import tkinter as tk
import customtkinter as cTk
from urllib.request import urlopen
from PIL import Image
import sqlite3 as sqlite3
import subprocess

finalapikey = ""
cTk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
cTk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(cTk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Džo baidens login peidž")
        self.geometry(f"{580}x{300}")
        self.resizable(False, False)
        
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)
        
        self.appnameframe = cTk.CTkFrame(self)
        self.appnameframe.grid(row=0, column=0, sticky="nsew", columnspan=2, padx=15, pady=10, ipadx=15, ipady=15)
        self.appnameframe.grid_rowconfigure(0, weight=1)
        self.appnameframe.grid_columnconfigure(0, weight=1)

        self.appnamelabel=cTk.CTkLabel(self.appnameframe, text="Counter Strike ieroču dizainu pārlukprogramma", font=("Comic Sans MS", 24))
        self.appnamelabel.grid(row=0, column=0)

        self.loginfieldframe = cTk.CTkFrame(self)
        self.loginfieldframe.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=15, pady=10, ipadx=15, ipady=15)

        self.loginusernamebox=cTk.CTkEntry(self.loginfieldframe, justify=tk.CENTER, placeholder_text="Lietotājvārds")
        self.loginpasswordbox=cTk.CTkEntry(self.loginfieldframe, justify=tk.CENTER, placeholder_text="Parole")
        self.loginbutton=cTk.CTkButton(self.loginfieldframe, text="Ienākt", command=self.launcher)
        self.registrationbutton=cTk.CTkButton(self.loginfieldframe, text="Reģistrēties", command=self.registrationlauncher)
        self.statustext=cTk.CTkLabel(self.loginfieldframe, text="")
        self.loginusernamebox.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.loginpasswordbox.grid(row=0, column=1, sticky="nsew", pady=10)
        self.loginbutton.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)
        self.registrationbutton.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)
        self.statustext.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)

    def registrationlauncher(self):
       subprocess.run(["python", "registration.py"])

    def launcher(self):
        username = self.loginusernamebox.get()
        password = self.loginpasswordbox.get()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('''SELECT * FROM usernames''')
        except:
            self.statustext.configure(text="Nav reģistrētu lietotāju datubāzē.", text_color="red")
            return

        info = c.fetchall()
        for row in info:
            if row[1]==username:
                if row[2]==password:
                    self.destroy()
                    c.execute("SELECT * FROM apikeys")
                    allapikeys = c.fetchall()
                    for apirow in allapikeys:
                        if apirow[0]==row[0]:
                            finalapikey=apirow[1]
                            print(finalapikey)
                            break
                    subprocess.run(["python", "main.py"])
                else:
                    self.statustext.configure(text="Nepareiza parole.", text_color="red")
            else:
                self.statustext.configure(text="Lietotājs neeksistē.", text_color="red")
                return




if __name__ == "__main__":
    app = App()
    app.mainloop()