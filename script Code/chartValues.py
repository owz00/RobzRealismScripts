import os
import pandas as pd
import sys
import csv
import numpy as np
import ast  # To safely convert string representations of lists

#this method converts the attributes of each breed to their respective charted values 
def convertChartValues(breedArray, functions):

# Read the equations from CSV and store them in a dictionary
    equations = {}
    with open(functions, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            col_name = row["statType"]
            equations[col_name] = eval(row["function"])  # Convert string to lambda function
    

    valueArray = np.zeros(len(breedArray))  # Initialize accumulation array with zeros


    for col, func in equations.items():
         if col in breedArray.columns:
            breedArray[col] = func(breedArray[col])  # Apply transformation
            breedArray[col] = breedArray[col].fillna(0)  # Replace NaN with 0
            valueArray += breedArray[col].values  # Sum element-wise

    return valueArray




def calculateSquadCosts(breedArray, squadArray, newValue):

    squad_selected = squadArray.loc[:, "c1":"c9"]
    breedName = breedArray['breedName'].to_numpy()
    breedValue = breedArray[f'{newValue}'].to_numpy()

    # Initialize a NumPy array to store summed MP values
    valueArray = np.zeros(len(squadArray))  

    for column in squad_selected.columns:  
        columnMpCost = np.zeros(len(squadArray))  # Ensure it's a NumPy array

        for index, value in squad_selected[column].items():
            value = ast.literal_eval(value)  # Convert string to tuple

            if value[0] != 'n/a':
                matchedIndex = np.where(breedName == value[0])[0]
                
                if len(matchedIndex) > 0:  # Ensure we found a match
                    mpValue = breedValue[matchedIndex][0]  # Extract MP value
                    mpCost = float(mpValue) * float(value[1])  
                    columnMpCost[index] = mpCost  # Store in NumPy array

        valueArray += columnMpCost  # Sum values row-wise across columns

    return valueArray  




def get_file_path(default_path):
    """Ask the user for a file path, defaulting to the provided path if left blank."""
    user_input = input(f"Enter file name/path for '{default_path}' (or press Enter to use default): ").strip()
    return user_input if user_input else default_path




def main():
    # Get the directory where the EXE is located
    if getattr(sys, 'frozen', False):  
        script_dir = os.path.dirname(sys.executable)  # Directory of the EXE
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script

    # Change the working directory to the script/executable location
    os.chdir(script_dir)
     

    # Get user-defined or default paths
    breed_file = get_file_path("RobzBreeds.csv")
    squad_file = get_file_path("RobzSquads.csv")
    mp_function = get_file_path("mp_functions.csv")
    cp_function= get_file_path("cp_functions.csv")
    # Read CSV and execute lambda functions

    # Load breed data
    breed_df = pd.read_csv(breed_file)
    convertedValues = pd.DataFrame(convertChartValues(breed_df, mp_function))
    convertedValues.columns = ["newMp"]
    breed_df = pd.concat([breed_df, convertedValues], axis=1)
    convertedValues = pd.DataFrame(convertChartValues(breed_df, cp_function))
    convertedValues.columns = ["newCp"]
    breed_df = pd.concat([breed_df, convertedValues], axis=1)
    
    # Save updated breed file
    breed_output = "RobzValue.csv"
    breed_df.to_csv(breed_output, index=False)
    print(f"Saved updated breed data to {breed_output}")

    # Load squad data
    squad_df = pd.read_csv(squad_file)
    newSquadValues = pd.DataFrame(calculateSquadCosts(breed_df, squad_df, 'newMp'))
    newSquadValues.columns = ["newSquadMp"]
    squad_df = pd.concat([squad_df, newSquadValues], axis=1)
    newSquadValues = pd.DataFrame(calculateSquadCosts(breed_df, squad_df, 'newCp'))
    newSquadValues.columns = ["newSquadCp"]
    squad_df = pd.concat([squad_df, newSquadValues], axis=1)
    
    # Save updated squad file
    squad_output = "NewRobzSquad.csv"
    squad_df.to_csv(squad_output, index=False)
    print(f"Saved updated squad data to {squad_output}")
    


  



if __name__ == "__main__":
    main()