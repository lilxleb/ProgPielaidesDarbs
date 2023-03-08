import tkinter
import tkinter.messagebox
import customtkinter as cTk
import requests
import csv
import os


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
        self.placeholder=["no weapon type has been selected"]
        
        # configure window
        self.title("Džo baidens")
        self.geometry(f"{1100}x{580}")
             
        #item dropdowna linki
        self.itemgetterframe = cTk.CTkFrame(self)
        self.itemgetterframe.grid(row=0, column=0, rowspan=4, sticky="nesw")
        #self.itemgetterframe.grid_rowconfigure(0, weight=1)
        #item dropdowni

        # typeName = self.getType()
        # selectedType=cTk.StringVar(value="")
        #taisīšu tikai rifles
        # #type dropdown
        # self.typeDropdown = cTk.CTkOptionMenu(self.itemgetterframe, variable=selectedType, values=typeName, command=self.updateWeaponName)
        # self.typeDropdown.grid(row=0, column=0)
        # self.typeDropdown.set("Rifle")

        csvFileName=''
        #gun dropdown
        self.weaponName=self.updateWeaponName("Rifle")
        selectedGun=cTk.StringVar(value="")
        self.weaponDropdown = cTk.CTkOptionMenu(self.itemgetterframe, variable=selectedGun, values=self.weaponName, command=self.updateSkinName)
        self.weaponDropdown.configure(values=self.updateWeaponName("Rifle")) #uzstāda viņu manuāli jo neeksistē vairāk iepriekšējais dropdowns
        self.weaponDropdown.set(self.weaponName[0])
        self.weaponDropdown.grid(row=0, column=0)

        #skin dropdown
        selectedSkin=cTk.StringVar(value="")
        self.skinDropdown = cTk.CTkOptionMenu(self.itemgetterframe, variable=selectedSkin, values=self.placeholder, command=self.updateAvailableWear)
        self.skinDropdown.grid(row=0, column=1)
        self.skinDropdown.set("Not Available")

        #wear dropdown
        selectedWear=cTk.StringVar(value="")
        self.wearDropdown = cTk.CTkOptionMenu(self.itemgetterframe, variable=selectedWear, values=self.placeholder)
        self.wearDropdown.grid(row=0, column=2)
        self.wearDropdown.set("Not Available")

        #load button
        self.loadButton = cTk.CTkButton(self.itemgetterframe, text="Load", command=self.apiRequest)
        self.loadButton.grid(row=0, column=3)
    


#---
#epic fucntions start here
#---

    def updateWeaponName(self, selectedType):
        with open('prog_piel\weaponvalues.csv', 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            returnList=[]
            for line in reader:
                if line['type']==selectedType:
                    returnList.append(line['wep_name'])
        returnList.sort()
        return returnList
    
    def updateSkinName(self, selectedGun):
        self.csvFileName=selectedGun.replace('-', '').lower()+".csv"
        with open(os.path.join("prog_piel/skins", self.csvFileName), 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            skinName=[]
            for line in reader:
                skinName.append(line['name'])
        skinName.sort()
        self.skinDropdown.configure(values=skinName)
        self.skinDropdown.set(skinName[0])

    def updateAvailableWear(self, selectedSkin):
        with open(os.path.join("prog_piel/skins", self.csvFileName), 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            lowest=0.0
            highest=0.0
            for line in reader:
                if line['name']==selectedSkin:
                    lowest=float(line['lowestf'])
                    highest=float(line['highestf'])
                    break
            
            wear_type_bounds = {
                "Factory New": [0.00, 0.07],
                "Minimal Wear": [0.07, 0.15],
                "Field-Tested": [0.15, 0.38],
                "Well Worn": [0.38, 0.45],
                "Battle Scarred": [0.45, 1.00]
            }
            returnWearTypes = []
            for wear_type, bounds in wear_type_bounds.items():
                if lowest <= bounds[1] and highest >= bounds[0]:
                    returnWearTypes.append(wear_type)
            self.wearDropdown.configure(values=returnWearTypes)
            self.wearDropdown.set(returnWearTypes[0])
               
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

    def apiRequest(self):
        pass
            
        


if __name__ == "__main__":
    app = App()
    app.mainloop()