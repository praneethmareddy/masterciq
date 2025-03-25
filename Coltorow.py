import pandas as pd
import os
import re

# Directories
ciq_folder = "./ciq_files/"
output_folder = "./output/"
os.makedirs(output_folder, exist_ok=True)
row_ciq_folder = os.path.join(output_folder, "row_ciqs")
os.makedirs(row_ciq_folder, exist_ok=True)

# Custom column lists
columns_to_add = ["extra_col1", "extra_col2"]  # Example additional columns to include
columns_to_remove = ["x_type", "y_param"]  # Example columns to exclude

# Define column groups to merge
column_groups = {
    "cellid": r'cellid\d+',    
    "cellname": r'cellname\d+' 
}

# Store CIQ summaries
ciq_column_summary = {}
row_ciq_column_summary = {}

# Process all CIQs in the folder
ciq_files = [file for file in os.listdir(ciq_folder) if file.endswith(".xlsx")]

for file in ciq_files:
    file_path = os.path.join(ciq_folder, file)
    df = pd.read_excel(file_path)

    # Store original column summary
    ciq_column_summary[file] = list(df.columns)

    # Identify grouped columns
    matched_columns = {group: [col for col in df.columns if re.match(pattern, col, re.IGNORECASE)]
                       for group, pattern in column_groups.items()}

    # Create row-wise structure
    row_columns = set(df.columns) - set(sum(matched_columns.values(), [])) - set(columns_to_remove)
    row_columns.update(columns_to_add)
    row_columns.update(column_groups.keys())  # Add merged column names

    # Store row-wise column summary
    row_ciq_column_summary[file] = list(row_columns)

    # Create new DataFrame with only row-wise columns
    row_df = pd.DataFrame(columns=row_columns)

    # Save Row CIQ
    row_ciq_path = os.path.join(row_ciq_folder, f"row_{file}")
    row_df.to_excel(row_ciq_path, index=False)

# Save Summary Sheets
summary_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in ciq_column_summary.items()]))
summary_df.to_excel(os.path.join(output_folder, "ciq_summary.xlsx"), index=False)

row_summary_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in row_ciq_column_summary.items()]))
row_summary_df.to_excel(os.path.join(output_folder, "row_ciq_summary.xlsx"), index=False)

print("✅ Summary sheets and row-wise CIQs generated successfully!")
