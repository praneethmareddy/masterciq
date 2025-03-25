import pandas as pd
import os
import re

# Directories
ciq_folder = "./ciq_files/"
output_folder = "./output/"
os.makedirs(output_folder, exist_ok=True)

# Custom column lists for adding/removing
columns_to_add = ["extra_col1", "extra_col2"]  # Example additional columns to include
columns_to_remove = ["x_type", "y_param"]  # Example columns to exclude

# Define column groups to merge
column_groups = {
    "cellid": r'cellid\d+',    # Matches cellid1, cellid2, cellid3...
    "cellname": r'cellname\d+' # Matches cellname1, cellname2, cellname3...
}

# Process all CIQs in the folder
ciq_files = [file for file in os.listdir(ciq_folder) if file.endswith(".xlsx")]

for file in ciq_files:
    file_path = os.path.join(ciq_folder, file)
    df = pd.read_excel(file_path)
    
    # Identify grouped columns
    matched_columns = {group: [col for col in df.columns if re.match(pattern, col, re.IGNORECASE)]
                       for group, pattern in column_groups.items()}
    
    # Check if any column groups are found
    if not any(matched_columns.values()):
        print(f"Skipping {file}: No relevant column groups detected.")
        continue

    # Stack relevant columns into a row-wise format
    stacked_data = []
    for _, row in df.iterrows():
        new_rows = []
        
        # Generate row-wise entries for each group
        for group, columns in matched_columns.items():
            for col in columns:
                if pd.notna(row[col]):
                    new_row = {group: row[col]}  # Rename column dynamically
                    new_rows.append(new_row)

        # Merge row-wise data with other relevant columns
        for new_row in new_rows:
            for existing_col in df.columns:
                if existing_col not in sum(matched_columns.values(), []) + columns_to_remove:
                    new_row[existing_col] = row[existing_col]

            stacked_data.append(new_row)

    row_wise_df = pd.DataFrame(stacked_data)

    # Add any extra columns
    for extra_col in columns_to_add:
        row_wise_df[extra_col] = None  # Empty column placeholder

    # Save the row-wise transformed CIQ
    output_file = os.path.join(output_folder, f"row_wise_{file}")
    row_wise_df.to_excel(output_file, index=False)

    print(f"Converted {file} to row-wise format and saved to {output_file}")

print("\nAll applicable CIQs processed and converted successfully!")
