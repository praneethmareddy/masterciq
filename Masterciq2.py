import pandas as pd
import glob
import os

# Folder containing CIQ Excel files
ciq_folder = "./ciq_files/"
output_folder = "./output/"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define exception mapping (treat equivalent column names as the same)
exception_map = {
    "SITEID": "HOSTSITEID",  # HOSTSITEID will be considered as the unique column
}

# Function to normalize column names
def normalize_column(col_name):
    col_name = col_name.replace(" ", "_").replace("-", "_").replace("/", "_").upper()
    return exception_map.get(col_name, col_name)  # Replace with mapped value if in exception list

# Get all Excel files in the folder
ciq_files = glob.glob(os.path.join(ciq_folder, "*.xlsx"))

# Dictionary to store original and normalized column names from each CIQ
ciq_columns = {}
unique_columns = set()

for file in ciq_files:
    df = pd.read_excel(file, nrows=0)  # Read only column names
    normalized_columns = [normalize_column(col) for col in df.columns]
    ciq_columns[os.path.basename(file)] = normalized_columns
    unique_columns.update(normalized_columns)

# Convert unique columns to a list (order is preserved)
unique_columns_list = list(unique_columns)

# Save column names to a text file
text_file_path = os.path.join(output_folder, "ciq_columns_summary.txt")
with open(text_file_path, "w") as f:
    for file, columns in ciq_columns.items():
        f.write(f"File: {file}\n")
        f.write(f"Columns after normalization: {', '.join(columns)}\n")
        f.write("-" * 50 + "\n")
    f.write("Unique Columns (after normalization):\n")
    f.write(", ".join(unique_columns_list) + "\n\n")
    f.write("Exception Mapping (Column Considered):\n")
    for original, final in exception_map.items():
        f.write(f"{original} → {final}\n")

# Save unique columns to CSV
csv_file_path = os.path.join(output_folder, "ciq_columns_summary.csv")
unique_columns_df = pd.DataFrame(columns=unique_columns_list)
unique_columns_df.to_csv(csv_file_path, index=False)

# Save normalized column names for each CIQ in a separate CSV
normalized_csv_path = os.path.join(output_folder, "ciq_normalized_columns.csv")
normalized_df = pd.DataFrame(dict([(file, pd.Series(columns)) for file, columns in ciq_columns.items()]))
normalized_df.to_csv(normalized_csv_path, index=False)

print(f"Column names summary saved to:\n- {text_file_path}\n- {csv_file_path}\n- {normalized_csv_path}")
