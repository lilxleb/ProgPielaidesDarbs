import tkinter as tk
import tkinter.messagebox
import customtkinter as cTk
import requests
import csv
import os
from urllib.request import urlopen
from PIL import Image
import io
import sqlite3 as sqlite3

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
        self.resizable(False, False)
             
        self.itemgetterframe = cTk.CTkFrame(self)
        self.itemgetterframe.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=10, ipadx=15, ipady=15)
        self.itemgetterframe.grid_columnconfigure((0,1,2,3,4), weight=1)     
        self.itemgetterframe.grid_rowconfigure(0, weight=1)

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
        
        self.imageFrame = cTk.CTkFrame(self)
        self.itemImage = cTk.CTkLabel(self.imageFrame, text="placeholder")
        self.imageFrame.grid(row=1, column=0, sticky='e', rowspan=3, padx=10)
        self.itemImage.grid(row=1, column=0, sticky="nsew", rowspan=3)

        self.dataFrame = cTk.CTkFrame(self)
        self.marketHashName = cTk.CTkLabel(self.dataFrame, text="placeholder")
        self.price = cTk.CTkLabel(self.dataFrame, text="placeholder")
        self.lore = cTk.CTkTextbox(self.dataFrame)
        self.collection = cTk.CTkLabel(self.dataFrame, text="placeholder")
        
        # Grid widgets
        self.dataFrame.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.marketHashName.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.price.grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.lore.grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.collection.grid(row=3, column=0, sticky='w', padx=10, pady=5)
        
        # Configure grid layout
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((1,2,3), weight=1)


    


#---
#epic fucntions start here
#---

    def updateWeaponName(self, selectedType):
        with open('weaponvalues.csv', 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            returnList=[]
            for line in reader:
                if line['type']==selectedType:
                    returnList.append(line['wep_name'])
        returnList.sort()
        return returnList
    
    def updateSkinName(self, selectedGun):
        self.csvFileName=selectedGun.replace('-', '').lower()+".csv"
        with open(os.path.join("skins", self.csvFileName), 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            skinName=[]
            for line in reader:
                skinName.append(line['name'])
        skinName.sort()
        self.skinDropdown.configure(values=skinName)
        self.skinDropdown.set(skinName[0])

    def updateAvailableWear(self, selectedSkin):
        with open(os.path.join("skins", self.csvFileName), 'r', encoding='UTF-8') as file:
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
        with open('weaponvalues.csv', 'r', encoding='UTF-8') as file:
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
        img_url = itemData['image']
        image_byt = urlopen(img_url).read()
        image_io = io.BytesIO(image_byt)
        pil_image = Image.open(image_io)

        skinImage = cTk.CTkImage(dark_image=pil_image, size=[512,384])
        self.itemImage.configure(image=skinImage)
        self.marketHashName.configure(text=itemData['market_hash_name'])
        self.price.configure(text=itemData['median_avg_prices_15days'][0][1])
        self.lore.configure(state="normal")
        self.lore.insert("0.0", str(itemData['assets']['descriptions'][2]['value']))
        self.lore.configure(state="disabled")
        print(itemData['assets']['descriptions'][2]['value'])
        if ifStatTrack==1:
            self.collection.configure(text=itemData['assets']['descriptions'][6]['value'])
            print(itemData['assets']['descriptions'])
        else:
            self.collection.configure(text=itemData['assets']['descriptions'][4]['value'])



        


if __name__ == "__main__":
    app = App()
    app.mainloop()