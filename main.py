import tkinter
import tkinter.messagebox
import customtkinter as cTk
import requests
import csv


secret = "zFAETYDs83HkjGk4ux82cGZvP90"

# ievads = input("ievadi skin nosaukumu: ")

# ievads=ievads.replace(" ", "%20").replace("|", "%7C").replace("(", "%28").replace(")", "%29")
# # ierocis | skinname (wear)

# response = requests.get(f"https://api.steamapis.com/market/item/730/{ievads}?api_key={secret}")
# skin=response.json()
# if response.status_code==400:
#     print("tu esi lohs")
#     print(ievads)
# else:
#     pp.pprint(f"{skin['market_name']} bilde: {skin['image']}")


cTk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
cTk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#global args

class App(cTk.CTk):
    def __init__(self):
        super().__init__()
        
        #args
        weaponName=['no weapon type has been selected']

        # configure window
        self.title("Džo baidens")
        self.geometry(f"{1100}x{580}")
             
        #item dropdowna linki
        self.itemgetterframe = cTk.CTkFrame(self)
        self.itemgetterframe.grid(row=0, column=0, rowspan=4, sticky="n")
        #item dropdowni

        typeName = self.getType()
        selectedType=cTk.StringVar(value="")

        self.typeDropdown = cTk.CTkOptionMenu(self.itemgetterframe, variable=selectedType, values=typeName, command=self.updateWeaponName)
        self.typeDropdown.grid(row=0, column=0)
        self.typeDropdown.set("Rifle")

        self.weaponDropdown = cTk.CTkOptionMenu(self.itemgetterframe, values=weaponName)
        self.weaponDropdown.grid(row=0, column=1)
        self.weaponDropdown.set("Not Available")
    
    def updateWeaponName(self, selectedType):
        with open('prog_piel\weaponvalues.csv', 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            returnList=[]
            for line in reader:
                if line['type']==selectedType:
                    returnList.append(line['wep_name'])
            self.weaponDropdown.configure(values=returnList)
            self.weaponDropdown.set(returnList[0])
    
    def getType(self):
        with open('prog_piel\weaponvalues.csv', 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            uniqueTypes=[]
            for line in reader:
                uniqueTypes.append(line['type'])
            uniqueTypes=set(uniqueTypes)
            uniqueTypes=[*uniqueTypes, ]
            return uniqueTypes
            #vajag lielos sākuma burtus + alfabēta secībā
        


if __name__ == "__main__":
    app = App()
    app.mainloop()