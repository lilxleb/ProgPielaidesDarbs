import tkinter as tk
import tkinter.messagebox
import customtkinter as cTk
import requests
import sqlite3 as sqlite3

cTk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
cTk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(cTk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Džo baidens login peidž")
        self.geometry(f"{300}x{300}")
        self.resizable(False, False)

        self.inputframe=cTk.CTkFrame(self)
        self.inputframe.grid(row=0, column=0)


        self.usernamehint=cTk.CTkLabel(self.inputframe, text="Lietotājvārds")
        self.keyhint=cTk.CTkLabel(self.inputframe, text="API atslēga")
        self.password1hint=cTk.CTkLabel(self.inputframe, text="Parole")
        self.password2hint=cTk.CTkLabel(self.inputframe, text="Atkārtojiet paroli")
        self.usernamehint.grid(row=0, column=0)
        self.keyhint.grid(row=1, column=0)
        self.password1hint.grid(row=2, column=0)
        self.password2hint.grid(row=3, column=0)
        
        self.username=cTk.StringVar(value="")
        self.apikey=cTk.StringVar(value="")
        self.password=cTk.StringVar(value="")
        self.password2=cTk.StringVar(value="")

        self.usernameinput=cTk.CTkEntry(self.inputframe, textvariable=self.username)
        self.keyinput=cTk.CTkEntry(self.inputframe, textvariable=self.apikey, show="*")
        self.password1input=cTk.CTkEntry(self.inputframe, textvariable=self.password, show="*")
        self.password2input=cTk.CTkEntry(self.inputframe, textvariable=self.password2, show="*")
        self.usernameinput.grid(row=0, column=1)
        self.keyinput.grid(row=1, column=1)
        self.password1input.grid(row=2, column=1)
        self.password2input.grid(row=3, column=1)

        self.checkerframe=cTk.CTkFrame(self)
        self.checkerframe.grid(row=1, column=0)

        self.apikeycheck=cTk.CTkButton(self.checkerframe, text="Pārbaudīt API atslēgu", command=self.checkapikey)
        self.registerbutton=cTk.CTkButton(self.checkerframe, text="Reģistrēties", state="Disabled", text_color="gray", command=self.register)
        self.statustext=cTk.CTkLabel(self.checkerframe, text=" ")
        self.apikeycheck.grid(row=0, column=0)
        self.registerbutton.grid(row=0, column=1)
        self.statustext.grid(row=1, column=0, columnspan=2)
        #self.checkerframe.rowconfigure((0, 1), weight=1)

    def checkapikey(self):
        apikey=self.keyinput.get()
        if apikey:
            link = "https://api.steamapis.com/market/item/730/AK-47%20%7C%20Gold%20Arabesque%20%28Factory%20New%29?api_key="
            response = requests.get(link+apikey)
            if response.status_code == 404 or response.status_code == 401:
                self.statustext.configure(text="Ievadīta nepareiza API atslēga vai API neiet!", text_color="red")
            elif response.status_code==200:
                self.statustext.configure(text="API atslēga apstiprināta!", text_color="green")
                self.registerbutton.configure(state="normal", text_color="white")
            else:
                self.statustext.configure(text="Kaut kas nav kārtībā.", text_color="red")
        else:
            self.statustext.configure(text="API atslēga nav ievadīta!", text_color="red")
    
    def register(self):
        pass
        



if __name__ == "__main__":
    app = App()
    app.mainloop()
