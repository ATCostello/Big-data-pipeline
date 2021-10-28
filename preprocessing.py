# Author: Alfred Costello, 35730761
# Created python script for SCC.411 groupwork to perform the pre-processing of the data according to the defined tasks.
import pandas as pd
import numpy as np
import os

print("- Pre-Processing starting")

# Read CSV files

inputdirectory = r'Original_Data'
outputdirectory = r'Processed_Data'

for filename in os.listdir(inputdirectory):
    if filename.endswith(".csv") and filename.startswith("part"):
        print("-- Pre-processing " + filename + " from directory " + inputdirectory)
        df = pd.read_csv(inputdirectory + '/' + filename, header=None)
        print(df.shape)
        
        # 2.2 Replace Hash Strings with numbers

        # Select all string columns
        dfobjects = df.select_dtypes(include='object')
        #print(dfobjects)

        # For each column that is a string - convert into a hash integer
        for col in dfobjects.columns: 
            df[col] = df[col].apply(hash)
        
        
        
        # 2.1 detect and remove outliers in the data

        def outlier_removal(datacolumn):
            sorted(datacolumn)
            Q1,Q3 = np.percentile(datacolumn , [10,90])
            IQR = Q3 - Q1
            lower_range = Q1 - (1.5 * IQR)
            upper_range = Q3 + (1.5 * IQR)
            return lower_range,upper_range

        for col in df.columns:
            lower_range,upper_range = outlier_removal(df[col])
            df.drop(df[ (df[col] > upper_range) | (df[col] < lower_range) ].index, inplace = True )
            
            
            
        # 2.4 Add new column to usage sheets processID = jobID + taskID
        #ONLY FOR TASK USAGE SPREADSHEETS
        if(filename.endswith("usage.csv")):
            df['processID'] = df[2] + df[3]
        
        
        
        # Write processed output sheets and 2.3 Convert scientific notation to float values
        print("--- Creating " + filename + " in directory " + outputdirectory)
        df.to_csv(outputdirectory + '/' + filename, float_format='%f', index=False, header=False)
        print(df.shape)
    else:
        continue
    
print("- Pre-Processing complete")
print("- Processed files output to " + outputdirectory)