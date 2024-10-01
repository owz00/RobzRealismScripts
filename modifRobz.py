import re
import os
import pandas as pd
import math
import tkinter as tk
from tkinter import simpledialog
import csv



def updateFile(fileName, newValueArray):

    regex = r'(.*mp\\.*)\\(\w*)\.set'
    fileString = ''
    #this code loosk for a difference in the breed name in the file path and the given breed name in the 'breedName' column
    #it is important to update the filepath column after updating the name
    newFileName = newValueArray[0]
    country = newValueArray[1]
      
    match = re.search(regex, fileName)
    directory = match.group(1)
    oldFileName = match.group(2) 

    

    if newFileName != oldFileName:
        print(oldFileName, newFileName)
            #changes the breed name on the breed file itself
            #-----------------------------------------------------------------
        try:
            os.rename(directory + '/' + oldFileName + '.set', directory + '/' + newFileName + '.set')
        except:
            print('an error occurred whilst renaming a file')
            #-----------------------------------------------------------------

            #-----------------------------------------------------------------
   

        vehicleFile = f'resource/set/multiplayer/units/{country}/vehicles.set'

        with open(vehicleFile, 'r') as file:
            fileString = ""
            lines = file.readlines()
            for line in lines:
                fileString += line

        with open(vehicleFile, 'w+') as file:         
            try:            
                newFileString = fileString.replace('(' + oldFileName + ':', '(' + newFileName +':')
                file.write(newFileString)
            except: 
                print("breed not found in vehciles file")

        try:
            #this try block looks for the breed name in the squads set and replaces all instances of it 
            directoryCountry = country
            if country == 'ger_ss':
               # print('hello')
                directoryCountry = 'ger'

            squadsFile = f'resource/set/multiplayer/units/{directoryCountry}/squads.set'
            with open(squadsFile, 'r') as file: #first read the contetns of a file
                fileString = ""
                lines = file.readlines()
                for line in lines:
                    fileString += line
            #print(directoryCountry)
            if directoryCountry == 'ger':
                regex = r'(side\('+ country + r'\).*?' + oldFileName + r'.*?f\()'
          
                match = re.search(regex, fileString) #return the correct breed section
                breedSection = match.group(1)
              

                newBreedSection = breedSection.replace('(' + oldFileName + ':',  '(' + newFileName + ':')
                newFileString = fileString.replace(breedSection, newBreedSection)

                with open(squadsFile, 'w+') as file:     
                    file.write(newFileString)
            else:
                with open(squadsFile, 'w+') as file:     
                    try:    
                        newFileString = fileString.replace('(' + oldFileName + ':', '(' + newFileName +':')
                        file.write(newFileString)
                    except: 
                          print("breed not found in squads file")
        except:
            ("squad file not found")
        
        soldierFile = 'resource/set/multiplayer/units/soldiers.set'
        with open(soldierFile, 'r') as file: #first read the contetns of a file
            fileString = ""
            lines = file.readlines()
            for line in lines:
                fileString += line
        with open(soldierFile, 'w+') as file:     
            try:    
                newFileString = fileString.replace(country + '/' + oldFileName + '"', country + '/' + newFileName + '"')
                file.write(newFileString)
            except: 
                 print("breed not found in soldiers file")
                 

        localizationFile = 'localization/desc.lng'
        with open(localizationFile, 'r') as file: #first read the contetns of a file
            fileString = ""
            lines = file.readlines()
            for line in lines:
                fileString += line
      

        regex = r'(\"' + country + r'\".*?\}\n\s*\})'
        match = re.search(regex, fileString, re.DOTALL)
        sectionString = match.group(1)
        
        newSectionString = sectionString.replace('"' + oldFileName + '"',  '"' + newFileName + '"')
        newFileString = fileString.replace(sectionString, newSectionString)

        with open(localizationFile, 'w+') as file:
            try:    
                file.write(newFileString)
            except: 
                 print("breed not found in desc.lng file")
            #-----------------------------------------------------------------
              

    
  
    return fileString
        
def getUserInput():
    directoryPath  = input("Enter directory path or 'd' for default path")

    if directoryPath == 'd':
        directoryPath = 'C:/Program Files (x86)/steam/steamapps/common/Men of War Assault Squad 2/mods/robz realism mod 1.29.5'
        #directoryPath = 'Desktop/robzScripts'
    else:
        return directoryPath 
    return directoryPath

def main():
    
    os.chdir(getUserInput())
    df = pd.read_csv("RobzBreeds.csv")
  
    filePaths = df['filePath'].values
    #warning- the order of this array is important
    array = df[['breedName', 'country']].values.tolist()

 
    print('updating files')
    for file, values in zip(filePaths, array):
       updateFile(file, values)
    print('files updated successfully')
    os.sleep(30)
    

  
if __name__ == "__main__":
    main()