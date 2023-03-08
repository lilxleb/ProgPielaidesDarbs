import tkinter
import tkinter.messagebox
import customtkinter as cTk
import requests
import csv
import os


secret = "zFAETYDs83HkjGk4ux82cGZvP90"


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
        self.wearDropdown = cTk.CTkOptionMenu(self.itemgetterframe, variable=selectedWear, values=self.placeholder, command=self.enableLoad)
        self.wearDropdown.grid(row=0, column=2)
        self.wearDropdown.set("Not Available")

        ifStatTrack=cTk.IntVar(value=0)
        self.stattrackCheckbox = cTk.CTkCheckBox(self.itemgetterframe, text="Stattrack?", variable=ifStatTrack, state="disabled", onvalue=1, offvalue=0)
        self.stattrackCheckbox.grid(row=0, column=3)

        #load button
        self.loadButton = cTk.CTkButton(self.itemgetterframe, text="Load", command=self.apiRequest, state='disabled')
        self.loadButton.grid(row=0, column=4)

        #--- display shit ---
        self.itemImage = cTk.CTkLabel(self, text="placeholder")
        self.marketHashName = cTk.CTkLabel(self, text="placeholder")
        self.price = cTk.CTkLabel(self, text="placeholder")
        self.lore = cTk.CTkLabel(self, text="placeholder")
        self.collection = cTk.CTkLabel(self, text="placeholder")
        
        # Grid widgets
        self.itemImage.grid(row=0, column=0, rowspan=4, padx=10)
        self.marketHashName.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        self.price.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        self.lore.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        self.collection.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    


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
            stattrack=0
            souvenir=0
            for line in reader:
                if line['name']==selectedSkin:
                    lowest=float(line['lowestf'])
                    highest=float(line['highestf'])
                    stattrack=int(line['stattrack'])
                    souvenir=int(line['souvenir'])
                    break
            
            wear_type_bounds = {
                "Factory New": [0.00, 0.07],
                "Minimal Wear": [0.07, 0.15],
                "Field-Tested": [0.15, 0.38],
                "Well-Worn": [0.38, 0.45],
                "Battle-Scarred": [0.45, 1.00]
            }
            returnWearTypes = []
            for wear_type, bounds in wear_type_bounds.items():
                if lowest <= bounds[1] and highest >= bounds[0]:
                    returnWearTypes.append(wear_type)

            self.wearDropdown.configure(values=returnWearTypes)
            self.wearDropdown.set(returnWearTypes[0])
            if souvenir==1:
                self.stattrackCheckbox.configure(state='normal')
                self.stattrackCheckbox.configure(text="Souvenir?")
            elif stattrack==1:
                self.stattrackCheckbox.configure(state='normal')
                self.stattrackCheckbox.configure(text="Stattrack?")
            elif souvenir==0 and stattrack==0:
                self.stattrackCheckbox.configure(state='disabled')
               
    def getType(self):
        with open('prog_piel\weaponvalues.csv', 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            uniqueTypes=[]
            for line in reader:
                uniqueTypes.append(line['type'])
            uniqueTypes=set(uniqueTypes)
            uniqueTypes=[*uniqueTypes, ]
            return uniqueTypes
    
    def enableLoad(self, selectedWear):
        self.loadButton.configure(state='normal')

    def apiRequest(self):
        weapon = self.weaponDropdown.get()
        skin = self.skinDropdown.get()
        wear = self.wearDropdown.get()
        ifStatTrack = self.stattrackCheckbox.get()
        if ifStatTrack==1 and self.stattrackCheckbox.cget('text')=="Stattrack?":
            print(self.stattrackCheckbox.cget('text'))
            requestString="StatTrak™ "+weapon+" | "+skin+" ("+wear+")"
        elif ifStatTrack==1 and self.stattrackCheckbox.cget('text')=="Souvenir?":
            print(self.stattrackCheckbox.cget('text'))
            requestString="Souvenir "+weapon+" | "+skin+" ("+wear+")"
        else:
            requestString=weapon+" | "+skin+" ("+wear+")" 
        requestString = requestString.replace(" ", "%20").replace("|", "%7C").replace("(", "%28").replace(")", "%29")

        response = requests.get(f"https://api.steamapis.com/market/item/730/{requestString}?api_key={secret}")
        itemData=response.json()
        self.itemImage.configure(text=itemData['image'])
        self.marketHashName.configure(text=itemData['market_hash_name'])
        self.price.configure(text=itemData['median_avg_prices_15days'][0][1])
        self.lore.configure(text=itemData['assets']['descriptions'][2]['value'])
        self.collection.configure(text=itemData['assets']['descriptions'][4]['value'])

    # def getUIElements(self, requestString):
    #     response = requests.get(f"https://api.steamapis.com/market/item/730/{requestString}?api_key={secret}")
    #     response.json()
    
    def loadImage(self, url):
        # TODO: Implement image loading
        pass
    
    def getRarityColor(self, rarity):
        # TODO: Implement rarity color coding
        return 'white'


        


if __name__ == "__main__":
    app = App()
    app.mainloop()