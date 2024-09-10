import tkinter as tk
from tkinter import simpledialog
import os 
import pandas as pd
import numpy as np
import re

#-----------------------------------------------------------------------------------------------------------------------------
#collect directory of the squad file for each country
def getSquadFiles(directory):
    squadFilePaths = []

    for root,d_names,f_names in os.walk(directory):  
                for file in f_names:
                    if re.search(r'.*squads.*', file):  #retrieve all these directories
                        filePath = os.path.join(root, file)
                        squadFilePaths.append(filePath)                 
    del squadFilePaths[0] #removes general squad file from directory array    
    return squadFilePaths
   

def getFiletext(squadFile): #this reads the file into string format
    with open(squadFile) as file:
            lines = file.readlines()
    return lines  
     

def retrieveSquads(directoryList):
    retrievedSquads = []

    for squadFile in directoryList: #this loop runs for each file , put the file text into a string format then searches for and then commits squads to an array 
        fileText = getFiletext(squadFile)
        for squadFile in fileText:
           squadList = re.findall(r'.*\(.*\)\s?', squadFile) #this line retrievs all squads within a file
           for squad in squadList:
               retrievedSquads.append(squad) 
               #print(squad)
    return retrievedSquads


def getUnlockTime(squad):
    regexPattern = r'.*\(.*c\((\d*).*f\((.*)\)\)\s?' #this finds the cooldown and fore values 
    match = re.search(regexPattern, squad, re.DOTALL)
    if match:     
        cooldown = int(match.group(1))
        fore = int(float(match.group(2)))
        unlockTime = cooldown - (fore * cooldown) #this formula returns the unlock time 
    else:
        unlockTime = "N/A"
    return unlockTime
 

def getSquadData(squadArray):
    dictionary = {'country':[], 'buyName':[], 'commandPower':[], 'score':[], 'captureWeight':[], 'cooldown':[],
                'mp':[], 'unlockTime':[], 'group':[], 'types':[],'c1':[],'c2':[],
                'c3':[], 'c4':[], 'c5':[], 'c6':[], 'c7':[], 'c8':[], 'c9':[]
                 };
    
    patterns = [(r'.*\(.*name\((\w*).*\)\s?',"buyName"),
                (r'.*\(.*side\((\w*).*\)\s?', "country"),
                (r'.*\(.*cost\((\w*).*\)\s?', "mp"),
                (r'.*\(.*c\((\w*).*\)\s?', "cooldown"),
                (r'.*\(\"(.*)\".*\)\s?', "types"),
                (r'.*\(.*g\((\w*)\)\s?', "group")
               ]
    
    breedPatterns = [(r'.*\(.*c1\((\w*)\:(\d*).*\)\s?', "c1"),
                     (r'.*\(.*c2\((\w*)\:(\d*).*\)\s?', "c2"),
                     (r'.*\(.*c3\((\w*)\:(\d*).*\)\s?', "c3"),
                     (r'.*\(.*c4\((\w*)\:(\d*).*\)\s?', "c4"),
                     (r'.*\(.*c5\((\w*)\:(\d*).*\)\s?', "c5"),
                     (r'.*\(.*c6\((\w*)\:(\d*).*\)\s?', "c6"),
                     (r'.*\(.*c7\((\w*)\:(\d*).*\)\s?', "c7"),
                     (r'.*\(.*c8\((\w*)\:(\d*).*\)\s?', "c8"),
                     (r'.*\(.*c9\((\w*)\:(\d*).*\)\s?', "c9")
                     ]
    
    for squad in squadArray: #this loop retrieves the required values from each squad and appends them into a dictionary
            dictionary["unlockTime"].append(getUnlockTime(squad))

            for pattern, key in breedPatterns:
                match = re.search(pattern, squad, re.DOTALL)
                if match:
                    matchValues = [match.group(1), match.group(2)]
                    dictionary[key].append(matchValues)
                else:
                    matchValues = ['n/a']      
                    dictionary[key].append(matchValues)
        

            for pattern, key in patterns:
                match = re.search(pattern, squad ,re.DOTALL)
                if match:
                    dictionary[key].append(match.group(1))
                else:
                    dictionary[key].append("N/A")
    return dictionary


def calculateSquadcosts(squadDictionary, breedDictionary):


    usedBreeds = []
    #gather the c1- c9 data, if n/a skip
    #match the breedNames up and retrieve the cp ,cw and score value
    #times these numbers by the second index in the 'c' array and add to all other 'c' types for the final result
    breedNames = breedDictionary['breedName']
    cp = breedDictionary['commandPower']
    score = breedDictionary['score']
    captureWeight = breedDictionary['captureWeight']

    squads = squadDictionary['buyName']

    c1 = squadDictionary['c1']
    c2 = squadDictionary['c2']
    c3 = squadDictionary['c3']
    c4 = squadDictionary['c4']
    c5 = squadDictionary['c5']
    c6 = squadDictionary['c6']
    c7 = squadDictionary['c7']
    c8 = squadDictionary['c8']
    c9 = squadDictionary['c9']

    cBreedArray = list(zip(c1, c2, c3, c4, c5, c6, c7, c8, c9))
   
    for arrays in cBreedArray:
        cpCost = 0
        sc = 0
        cw = 0
        for arr in arrays:
            if arr[0] != 'n/a':
                try:
                    matchedIndex = breedNames.index(arr[0])
                    usedBreeds.append(arr[0])
                    cpCost = cpCost + int(arr[1]) * float(cp[int(matchedIndex)])
                    sc = sc + int(arr[1]) * float(score[int(matchedIndex)])
                    cw = cw + int(arr[1]) * float(captureWeight[int(matchedIndex)])
                except:
                    cpCost = 'n/a'
                    sc = 'n/a'
                    cw = 'n/a'
        #print(cpCost)
        squadDictionary['commandPower'].append(cpCost)      
        squadDictionary['score'].append(sc) 
        squadDictionary['captureWeight'].append(cw)  
    

    unusedBreeds = getUnusedBreeds(usedBreeds, breedNames)
    return squadDictionary, unusedBreeds

#-----------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------
def getBreedFiles(directory):
    breedFilePaths = []
   
    for root,d_names,f_names in os.walk(directory):  
                for file in f_names:
                    if file.endswith(".set"):
                        filePath = os.path.join(root, file)
                        breedFilePaths.append(filePath)                 
 
    return breedFilePaths
     
     
def extractBreedData(breedFiles):
    
    breedInventory = []
    breedDictionary = {"country":[], "breedName":[],"health":[], "finalSkill":[], "veterancy":[],
                            "healthRegen":[], "staminaRegen":[], "speed":[], "inventory":[],
                            "tankSkill":[], "vehicleSkill":[], "cannonSkill":[], "tankGunSkill":[], "pistolSkill":[],
                            "smgSkill":[], "mgunSkill":[], "rifleSkill":[], "rocketLskill":[],
                            "melee":[], "commandPower":[], "score":[], "captureWeight":[]}
        
    patterns = [(r'.*health\"\s\"(\d*).*',"health"),
                (r'.*health_regeneration\"\s\"(\d*).*',"healthRegen"),
                (r'.*stamina_regeneration\"\s\"(\d*).*',"staminaRegen"),
                (r'speed\"\s*(.*)\s',"speed"),
                (r'tank\"\s*(.*)\s',"tankSkill"),
                (r'vehicle\"\s*(.*)\s',"vehicleSkill"),
                (r'cannon\"\s*(.*)\s',"cannonSkill"),
                (r'pistol.*lvl\_(\d*)',"pistolSkill"),
                (r'smg.*lvl\_(\d*)',"smgSkill"),
                (r'mgun.*lvl\_(\d*)',"mgunSkill"),
                (r'rifle.*lvl\_(\d*)',"rifleSkill"),
                (r'tankgun.*lvl\_(\d*)',"tankGunSkill"),
                (r'rocketlauncher.*lvl\_(\d*)',"rocketLskill"),
                (r'melee.*lvl\_(\d*)',"melee"),
                (r'\(\"veterancy_(.*?)\"',"veterancy"),
                ]

    inventoryPattern = r'item\s(.*?)\}'    

    for breedFile in breedFiles:
        fileString = ""

        match = re.search(r'.*mp\\(.*)\\(\w*).set', breedFile)
        country = match.group(1)
        entityName = match.group(2)
        
        
        with open(breedFile) as file:
            #add all lines of the text file to a string
            lines = file.readlines()
            for line in lines:
                fileString += line

        inventoryItems = re.findall(inventoryPattern, fileString)
        breedDictionary["inventory"].append(inventoryItems)
        
        for pattern, key in patterns:
            match = re.search(pattern, fileString )
            if match:
                breedDictionary[key].append(match.group(1))
            else:
                breedDictionary[key].append("n/a")

        breedDictionary["breedName"].append(entityName)  
        breedDictionary["country"].append(country)  
          
    return breedDictionary


def addfinalSkilltoBreed(breedDictionary, soldierDictionary, finalSkillDictionary):

    breeds = breedDictionary['breedName']
    soldier = soldierDictionary['breedName']
    soldierVeterancy  = soldierDictionary['finalSkill']
    
    #for every breed in breedDictionay i retrieve the index of its match in the soldierDictionary. 
    #Using the index i then retrieve the veterancy value and the same index and append it to the breedDictionary
    for breed in breeds:
        try:
            matchedIndex = soldier.index(breed)
            breedDictionary['finalSkill'].append(soldierVeterancy[matchedIndex])
        except:
            matchedIndex = 'n/a'
            breedDictionary['finalSkill'].append(matchedIndex)    


   ##then add the other veterancy values from the veterancy dictionary 
    breedFinalSkill  = breedDictionary['finalSkill']
    veterancy = finalSkillDictionary['veterancyName']

    vCp = finalSkillDictionary["commandPower"]
    vScore = finalSkillDictionary["score"]
    vCW = finalSkillDictionary["captureWeight"]

    #for every breed in breedDictionay i retrieve the index of its match (using the names of the breed) in the soldierDictionary. 
    #Using the index i then retrieve the relevant values from veterancy and append them into the breedDictionary 
    for breedVet in breedFinalSkill:
        try:
            matchedIndex = veterancy.index(breedVet)
            breedDictionary['commandPower'].append(vCp[matchedIndex])
            breedDictionary['score'].append(vScore[matchedIndex])
            breedDictionary['captureWeight'].append(vCW[matchedIndex])
        except:
            matchedIndex = 'n/a'
            breedDictionary['commandPower'].append(matchedIndex)
            breedDictionary['score'].append(matchedIndex)
            breedDictionary['captureWeight'].append(matchedIndex)

    return breedDictionary      
     
#-----------------------------------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------------------------------
def extractSoldierData(directory):
    fileString= ""
    soldierList = []
    finalSkillDictionaryList = []

    soldierDictionary = {'breedName':[], 'finalSkill':[], 'captureWeight':[], 'commandPower':[], 'score':[]}
    finalSkillDictionary = {'veterancyName':[], 'captureWeight':[], 'commandPower':[], 'score':[]}

    with open(directory) as file:
            #add all lines of the text file to a string
        lines = file.readlines()
        for line in lines:
            fileString += line
    
    finalSkillDictionaryList = re.findall(r'define.*?\)', fileString, re.DOTALL)
    for finalSkillLevel in finalSkillDictionaryList:
        match = re.search(r'define\s\"(\w*)\".*cp\s*(.*?)\}.*score\s*(.*?)\}.*cw\s*(.*?)\}', finalSkillLevel, re.DOTALL)
        if match:
            finalSkillDictionary["veterancyName"].append(match.group(1))
            finalSkillDictionary["commandPower"].append(match.group(2))
            finalSkillDictionary["score"].append(match.group(3))
            finalSkillDictionary["captureWeight"].append(match.group(4))
        else:
            finalSkillDictionary["veterancyName"].append('n/a')
            finalSkillDictionary["commandPower"].append('n/a')
            finalSkillDictionary["score"].append('n/a')
            finalSkillDictionary["captureWeight"].append('n/a')
                                                              
   
    soldierList = re.findall(r'\"mp.*?\)', fileString) #this line retrieevs all sqauds within a file
    for soldier in soldierList:
        match = re.search(r'\"mp\/.*\/(\w*)\".*\(\"(.*)\"', soldier)
        if match:
            soldierDictionary["breedName"].append(match.group(1))
            soldierDictionary["finalSkill"].append(match.group(2))
        else:
            soldierDictionary["breedName"].append('n/a')
            soldierDictionary["finalSkill"].append('n/a')

    
        
    return soldierDictionary, finalSkillDictionary    
#-----------------------------------------------------------------------------------------------------------------------------    


#-----------------------------------------------------------------------------------------------------------------------------          
     
def getVeterancy(veterancyDirectory):
    fileString = ""

    with open(veterancyDirectory) as file:
        #add all lines of the text file to a string
        lines = file.readlines()
        for line in lines:
            fileString += line


    veterancyDictionary = {"veterancyLevel": [], "health":[], "healthRegen":[],  "stamina":[],  "staminaRegen":[],  "tank":[], 
                            "vehicle":[],  "cannon":[],  "weaponReload":[],  "weaponSkill":[]}
    
    veterancyLevelList = []

    levelList = re.findall(r'\"lvl_.*?weapon_skill.*?\}', fileString, re.DOTALL) #this line retrievs all veterancies within a file
    for veterancyLevel in levelList:
        veterancyLevelList.append(veterancyLevel) 


    patterns = [(r'\"(.*?)\"\s*from\s*veterancy',"veterancyLevel"),
                (r'\"weapon_reload\"\s*(.*)\}',"weaponReload"),
                (r'\"weapon_skill\"\s*(.*)\}',"weaponSkill"),
                (r'\"cannon\"\s*(.*)\}',"cannon"),
                (r'\"vehicle\"\s*(.*)\}',"vehicle"),
                (r'\"tank\"\s*(.*)\}',"tank"),
                (r'\"stamina_regeneration\"\s*(.*)\}',"staminaRegen"),
                (r'\"stamina\"\s*(.*)\}',"stamina"),
                (r'\"health_regeneration\"\s*(.*)\}',"healthRegen"),
                (r'\"health\"\s*(.*)\}',"health")
                ]    

    for veterancyLevel in veterancyLevelList:
        #print(veterancyLevel)
        for pattern, key in patterns:
            match = re.search(pattern, veterancyLevel)
            if match:
                veterancyDictionary[key].append(match.group(1))
            else:
                veterancyDictionary[key].append("n/a")

    return veterancyDictionary
#-----------------------------------------------------------------------------------------------------------------------------  

#-----------------------------------------------------------------------------------------------------------------------------  
def getUnusedBreeds(usedBreeds, breedNames):
    unusedBreeds = []
    for breed in breedNames:
        try:
            usedBreeds.index(breed)
        except:
            unusedBreeds.append(breed)
    return unusedBreeds



def deleteFiles(unusedBreeds):
    breedDirectoryD = ["./set/breed/mp/jap/",
                       "./set/breed/mp/eng/",
                       "./set/breed/mp/rus/",
                       "./set/breed/mp/ger/",
                       "./set/breed/mp/ger2/",
                       "./set/breed/mp/ger_ss/",
                       "./set/breed/mp/usa/",
                       "./set/breed/mp/rus_guard/"
    ]

   # print(os.getcwd())
    #os.remove("./set/breed/mp/eng/elite4.set")
    #
    for breed in unusedBreeds:
        for filePath in breedDirectoryD:
            try:
               breedDirectory = filePath + breed + ".set"
               os.remove(breedDirectory)
               print("deleted")
            except:
              print("0")
#-----------------------------------------------------------------------------------------------------------------------------  


#-----------------------------------------------------------------------------------------------------------------------------  
def getUserInput():

    directoryPath  = input("Enter directory path or 'd' for default path")

    if directoryPath == 'd':
        directoryPath = 'C:/Program Files (x86)/steam/steamapps/common/Men of War Assault Squad 2/mods/robz realism mod 1.29.5/resource'
    else:
        return directoryPath 

    
    return directoryPath 


#-----------------------------------------------------------------------------------------------------------------------------  




#-----------------------------------------------------------------------------------------------------------------------------
def main():
    
    os.chdir(getUserInput())
    breedDirectory = "./set/breed/mp"
    breedFiles = getBreedFiles(breedDirectory)
    breedDictionary = extractBreedData(breedFiles)
    #print(breedDictionary)

    soldierDirectory = "./set/multiplayer/units/soldiers.set"
    soldierDictionary,  finalSkillDictionary = extractSoldierData(soldierDirectory)
    breedDictionary = addfinalSkilltoBreed(breedDictionary, soldierDictionary, finalSkillDictionary)
    #print(breedDictionary)

    squadArray = []
    squadDirectory = "./set/multiplayer/units"
    squadFiles = getSquadFiles(squadDirectory)
    squadArray = retrieveSquads(squadFiles)
    squadDictionary = getSquadData(squadArray)
    squadDictionary, unusedBreeds = calculateSquadcosts(squadDictionary, breedDictionary)
    #print(squadDictionary)

    veterancyDirectory = "./set/ability/veterancy.set"
    veterancyDictionary = getVeterancy(veterancyDirectory)
    #print(veterancyDictionary)


    data_frame = pd.DataFrame(unusedBreeds)
    data_frame.to_csv('UnusedBreeds.csv', index=False)
    print('DataFrame has been written to Excel File successfully.')

    #deleteFiles(unusedBreeds)
    #print("Files Deleted")



    data_frame = pd.DataFrame(squadDictionary)
    data_frame.to_csv('RobzSquadss.csv', index=False)
    print('DataFrame has been written to Excel File successfully.')

    data_frame = pd.DataFrame(breedDictionary)
    data_frame.to_csv('RobzBreeds.csv', index=False)
    print('DataFrame has been written to Excel File successfully.')


    data_frame = pd.DataFrame(finalSkillDictionary)
    data_frame.to_csv('RobzVet.csv', index=False)
    print('DataFrame has been written to Excel File successfully.')


if __name__ == "__main__":
    main()
#-----------------------------------------------------------------------------------------------------------------------------

#collect breed data in dictionary
#for each value key name collect all breed values
#using the breed names find the corresponding breed name and collect its data
#