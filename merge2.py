#!/usr/bin/env python3

import os
import pandas as pd

# Define the parent directory where subfolders are located
parent_dir = '/home/omicslogic/Variant_Allele_Filtered_Data_NP'

# Initialize an empty DataFrame to store merged data
merged_df = pd.DataFrame()

# Loop through all subdirectories and files
for root, dirs, files in os.walk(parent_dir):
    for file in files:
        if file.endswith('.xlsx'):
            # Get the folder name and file name
            folder_name = os.path.basename(root)
            file_name = os.path.splitext(file)[0]
            
            # Create the full file path
            file_path = os.path.join(root, file)
            
            # Ensure that the file exists before attempting to read it
            if os.path.exists(file_path):
                try:
                    # Read the current Excel file
                    df = pd.read_excel(file_path)
                    
                    # Add folder and file name as new columns
                    df.insert(0, 'Folder', folder_name)
                    df.insert(1, 'File', file_name)
                    
                    # Concatenate the data vertically (axis=0) (stack rows)
                    merged_df = pd.concat([merged_df, df], axis=0, ignore_index=True)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

# Optionally, save the merged data to a new CSV file
merged_df.to_csv('/home/omicslogic/merged_variant_data_vertical.csv', index=False)

# Print the first few rows of the merged DataFrame
#print(merged_df.head())
