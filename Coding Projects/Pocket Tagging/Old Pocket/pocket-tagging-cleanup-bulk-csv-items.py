import os
import csv
import glob
import re

# Define folder and file paths
POCKET_FOLDER = (
    "/Users/h3p/Coding/New-Coding-Universal/Coding Projects/Pocket Tagging/pocket"
)
OUTPUT_CSV = os.path.join(POCKET_FOLDER, "updated_pocket_data.csv")

# Create pocket folder if it doesn't exist
os.makedirs(POCKET_FOLDER, exist_ok=True)


def extract_title_from_url(url):
    """Extract a simple title from a URL using the last path segment or domain."""
    # Remove protocol and www
    url_cleaned = re.sub(r"^https?://(www\.)?", "", url).strip("/")
    # Split by '/' and take the last non-empty segment
    parts = url_cleaned.split("/")
    for part in reversed(parts):
        if part and not part.startswith(
            ("?", "#")
        ):  # Ignore query strings or fragments
            # Remove file extensions (e.g., .html, .php) and replace hyphens/underscores with spaces
            title = re.sub(r"\.(html|php|aspx|jsp)$", "", part)
            title = re.sub(r"[-_]+", " ", title).capitalize()
            return title
    # Fallback: use the domain if no meaningful path
    return url_cleaned.split("/")[0].capitalize()


def process_csv_files():
    """Process all CSV files in the pocket folder and update titles."""
    csv_files = glob.glob(os.path.join(POCKET_FOLDER, "*.csv"))
    if not csv_files:
        print(
            f"Warning: No .csv files found in {POCKET_FOLDER}. Please add your Pocket export CSV(s)."
        )
        return

    all_rows = []
    for csv_file in csv_files:
        print(f"Processing {csv_file}...")
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Verify expected columns
            expected_columns = {"title", "url", "time_added", "tags", "status"}
            if not expected_columns.issubset(reader.fieldnames):
                print(
                    f"Error: {csv_file} does not have the expected columns: {expected_columns}"
                )
                continue

            for row in reader:
                # Check if title is a URL
                if row["title"].startswith(("http://", "https://")):
                    # Extract title from the URL column
                    new_title = extract_title_from_url(row["url"])
                    print(
                        f"Updated title from '{row['title']}' to '{new_title}' for URL: {row['url']}"
                    )
                    row["title"] = new_title
                all_rows.append(row)
        print(f"Loaded {len(all_rows)} rows from {os.path.basename(csv_file)} so far.")

    if not all_rows:
        print("No rows processed. Exiting.")
        return

    # Write updated data to a new CSV
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["title", "url", "time_added", "tags", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Saved {len(all_rows)} updated rows to {OUTPUT_CSV}.")


if __name__ == "__main__":
    process_csv_files()
