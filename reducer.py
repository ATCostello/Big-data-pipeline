# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 17:18:31 2021

@author: Alf
"""

#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np

# Take a single key (filename) from stdin and split
for input_line in sys.stdin:
    input_line = input_line.strip()
    key, value = input_line.split("\t", 1)
    value = int(value)
   
    print("- Pre-Processing starting")
    
    
    # Read CSV files
    
    inputdirectory = r'Original_Data'
    outputdirectory = r'Processed_Data'
    
    if key.endswith(".csv") and key.startswith("part"):
        print("-- Pre-processing " + key + " from directory " + inputdirectory)
        df = pd.read_csv(inputdirectory + '/' + key, header=None)
        print(df.shape())
        # 2.2 Replace Hash Strings with numbers
    
        # Select all string columns
        dfobjects = df.select_dtypes(include='object')
        #print(dfobjects)
    
        # For each column that is a string - convert into a hash integer
        for col in dfobjects.columns: 
            df[col] = df[col].apply(hash)
            
            
            
        # 2.1 detect and remove outliers in the data
    
        def outlier_treatment(datacolumn):
            sorted(datacolumn)
            Q1,Q3 = np.percentile(datacolumn , [10,90])
            IQR = Q3 - Q1
            lower_range = Q1 - (1.5 * IQR)
            upper_range = Q3 + (1.5 * IQR)
            return lower_range,upper_range
    
        for col in df.columns:
            lower_range,upper_range = outlier_treatment(df[col])
            df.drop(df[ (df[col] > upper_range) | (df[col] < lower_range) ].index, inplace = True )
                
                
                
        # 2.4 Add new column to usage sheets processID = jobID + taskID
        #ONLY FOR TASK USAGE SPREADSHEETS
        if(key.endswith("usage.csv")):
            df['processID'] = df[2] + df[3]
            
            
            
        # Write processed output sheets and 2.3 Convert scientific notation to float values
        print("--- Creating " + key + " in directory " + outputdirectory)
        df.to_csv(outputdirectory + '/' + key, float_format='%f', index=False, header=False)
        print(df.shape())
        
    print("- Pre-Processing complete")
    print("- Processed files output to " + outputdirectory)