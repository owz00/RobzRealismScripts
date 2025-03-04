import os
import re
import pandas as pd
import numpy as np 
import math
import sys

def updateSquad(squad, newSquads):
      
      squadNames = newSquads['buyName'].to_numpy()
      squadMp = newSquads['newSquadMp'].to_numpy()
      country = newSquads['country'].to_numpy()

      #find the squad name 
      pattern = r'.*\(.*name\((\w*).*\)\s?'
      squadName =  re.search(pattern, squad, re.DOTALL) 
      #find the country name
      pattern = r"(?:side|s)\((\w+)\)"
      countryName =  re.search(pattern, squad, re.DOTALL)

      if squadName:
          # Retrieve MP value
          mp_value = newSquads.loc[(newSquads["country"] == countryName.group(1)) & 
                                   (newSquads["buyName"] == squadName.group(1)), "newSquadMp"]
    
          mp_value = mp_value.iloc[0] if not mp_value.empty else None
      
          mp_value = math.ceil(int(mp_value))

          #replace the old mp value with the new one
          mpPattern = r"(cost\()\d+(\))"

          # Replace the cost value while keeping the surrounding text unchanged
          updated_text = re.sub(mpPattern, 'cost(' + str(mp_value) + ')', squad)
 
   
      else:
         updated_text = squad
        
      return updated_text
    

def getSquadFiles(directory):
    squadFilePaths = []
    for root,d_names,f_names in os.walk(directory):  
                for file in f_names:
                    if re.search(r'.*squads.*', file):  #retrieve all these directories
                        filePath = os.path.join(root, file)
                        squadFilePaths.append(filePath)                 
    del squadFilePaths[0] #removes general squad file from directory array    
    return squadFilePaths


#this method retrieves the chunks of text which describe the squad attributes 
def modifySquads(directoryList, newSquads):
    retrievedSquads = []
    for squadFile in directoryList: #this loop runs for each file , put the file text into a string format then searches for and then commits squads to an array 
        fileText = getFiletext(squadFile)

        squadList = re.findall(r'.*\(.*\)\s?', fileText) #this line retrievs all squads within a file
        for squad in squadList:
            squad = squad.rstrip()
            updatedSquad = updateSquad(squad, newSquads)
           
            fileText = fileText.replace(squad, updatedSquad)
        with open(squadFile, 'w+') as file:         
            try:      
                file.write(fileText)
            except: 
                print("unable to write to file")        
    return fileText


def getFiletext(squadFile): #this reads the file into string format
    fileString = ""
    with open(squadFile) as file:
            lines = file.readlines()
            for line in lines:
                fileString += line
    return fileString  


def get_file_path(default_path):
    """Ask the user for a file path, using the default if left blank."""
    user_input = input(f"Enter file path for '{default_path}' (or press Enter to use default): ").strip()
    return user_input if user_input else default_path


def main():
    # Get the directory where the EXE is located
    if getattr(sys, 'frozen', False):  
        script_dir = os.path.dirname(sys.executable)  # Directory of the EXE
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script

    # Change the working directory to the script/executable location
    os.chdir(script_dir)

    # Ask for file paths
    squads_file = get_file_path("NewRobzSquad.csv")
    units_folder = get_file_path("./resource/gamelogic/set/multiplayer/units")

    # Load new squad data
    newSquads = pd.read_csv(squads_file)
    # Retrieve squad file paths
    squadFilePaths = getSquadFiles(units_folder)
    # Modify Squad Files
    modifySquads(squadFilePaths, newSquads)
  
    print("Squad processing completed.")


if __name__ == "__main__":
    main()