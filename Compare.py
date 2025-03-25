import pandas as pd
import itertools
import os
import seaborn as sns
import matplotlib.pyplot as plt

# File paths
ciq_columns_csv = "./output/ciq_columns_summary.csv"  # CSV containing all column names
output_folder = "./output/"
os.makedirs(output_folder, exist_ok=True)

# Load the column names
df = pd.read_csv(ciq_columns_csv)

# Extract column names from each CIQ (columns stored row-wise)
ciq_column_groups = {f"CIQ_{i+1}": set(df.iloc[:, i].dropna()) for i in range(df.shape[1])}

# Pairwise comparison storage
pairwise_comparison = []
print("\nPAIRWISE CIQ COLUMN MAPPING:")

for (ciq1, cols1), (ciq2, cols2) in itertools.combinations(ciq_column_groups.items(), 2):
    common_columns = cols1 & cols2
    unique_to_ciq1 = cols1 - cols2
    unique_to_ciq2 = cols2 - cols1

    # Print pairwise mapping
    print(f"\n{ciq1} Columns: {sorted(list(cols1))}")
    print(f"{ciq2} Columns: {sorted(list(cols2))}")
    print(f"Common Columns ({len(common_columns)}): {sorted(list(common_columns))}")
    print(f"Unique to {ciq1} ({len(unique_to_ciq1)}): {sorted(list(unique_to_ciq1))}")
    print(f"Unique to {ciq2} ({len(unique_to_ciq2)}): {sorted(list(unique_to_ciq2))}")

    # Store in DataFrame format
    pairwise_comparison.append({
        "CIQ_1": ciq1, "CIQ_2": ciq2,
        "Common Columns Count": len(common_columns),
        "Unique to CIQ_1": len(unique_to_ciq1),
        "Unique to CIQ_2": len(unique_to_ciq2),
        "Common Columns": ", ".join(common_columns),
        f"Unique to {ciq1}": ", ".join(unique_to_ciq1),
        f"Unique to {ciq2}": ", ".join(unique_to_ciq2)
    })

# Convert to DataFrame
pairwise_df = pd.DataFrame(pairwise_comparison)

# Save results to CSV
pairwise_csv_path = os.path.join(output_folder, "pairwise_comparison.csv")
pairwise_df.to_csv(pairwise_csv_path, index=False)

# Create a heatmap of common column counts
heatmap_data = pd.DataFrame(index=ciq_column_groups.keys(), columns=ciq_column_groups.keys(), dtype=int).fillna(0)

for _, row in pairwise_df.iterrows():
    heatmap_data.loc[row["CIQ_1"], row["CIQ_2"]] = row["Common Columns Count"]
    heatmap_data.loc[row["CIQ_2"], row["CIQ_1"]] = row["Common Columns Count"]

# Visualizing common columns count using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, cmap="Blues", fmt="d", linewidths=0.5)
plt.title("Pairwise Common Column Counts Across CIQs")
plt.xlabel("CIQs")
plt.ylabel("CIQs")

# Save and display the heatmap
heatmap_path = os.path.join(output_folder, "common_columns_heatmap.png")
plt.savefig(heatmap_path)
plt.show()

print(f"\nPairwise comparison saved to {pairwise_csv_path}")
print(f"Heatmap saved to {heatmap_path}")
