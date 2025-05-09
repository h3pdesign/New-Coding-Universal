import os
import csv
import glob

# Define folder and file paths
POCKET_FOLDER = (
    "/Users/h3p/Coding/New-Coding-Universal/Coding Projects/Pocket Tagging/pocket"
)
OUTPUT_CSV = os.path.join(POCKET_FOLDER, "filtered_pocket_data.csv")

# Create pocket folder if it doesn't exist
os.makedirs(POCKET_FOLDER, exist_ok=True)


def filter_csv_files():
    """Process all CSV files in the pocket folder and remove rows with 'flip.it' in the URL."""
    csv_files = glob.glob(os.path.join(POCKET_FOLDER, "*.csv"))
    if not csv_files:
        print(
            f"Warning: No .csv files found in {POCKET_FOLDER}. Please add your Pocket export CSV(s)."
        )
        return

    all_rows = []
    filtered_count
