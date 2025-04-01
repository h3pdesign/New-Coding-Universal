import os
import time
import re
import json
import unicodedata
import csv
import glob
import spacy

try:
    from pocket import Pocket
except ImportError:
    print("Error: 'pocket' library is not installed. Run 'pip install pocket'.")
    exit(1)
from dotenv import load_dotenv

# Load spaCy German model (for German and English content)
nlp = spacy.load("de_core_news_sm")

# Load environment variables from default .env file
load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing Pocket environment variables. Check your .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)

# Define folder and file paths
POCKET_FOLDER = "pocket"
TAG_MAPPING_FILE = os.path.join(POCKET_FOLDER, "tag_mapping.json")
TAGGED_EXPORT_FILE = os.path.join(POCKET_FOLDER, "tagged_pocket_data.json")

# Create pocket folder if it doesn't exist
os.makedirs(POCKET_FOLDER, exist_ok=True)


def clean_tag(tag):
    """Clean and normalize a tag."""
    normalized = "".join(
        c for c in unicodedata.normalize("NFKD", tag) if unicodedata.category(c) != "Mn"
    )
    unwanted = r"[°€?!@#$%^&*()+={}[\]|\\:;\"'<>,./\s]+"
    cleaned = re.sub(unwanted, "-", normalized).lower().strip("-")
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned if cleaned and len(cleaned) <= 50 else ""


def extract_keywords_from_text(text):
    """Extract keywords from text using spaCy."""
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if (
            token.pos_ in ["NOUN", "PROPN"]
            and not token.is_stop
            and len(token.text) > 2
        ):
            keywords.add(token.lemma_.lower())
    return keywords


def map_to_common_tags(keywords):
    """Map keywords to a curated set of common tags."""
    tag_mapping = {
        # Broad categories with keyword triggers
        "technologie": [
            "tech",
            "technology",
            "coding",
            "code",
            "software",
            "hardware",
            "ai",
            "ki",
            "internet",
            "digital",
        ],
        "wissenschaft": [
            "science",
            "research",
            "study",
            "experiment",
            "theory",
            "quantum",
            "physik",
        ],
        "medizin": [
            "health",
            "medicine",
            "ketamine",
            "dopamine",
            "brain",
            "therapy",
            "disease",
            "gesundheit",
        ],
        "energie": [
            "energy",
            "tokamak",
            "fusion",
            "reactor",
            "power",
            "solar",
            "wind",
            "nuclear",
        ],
        "geschichte": [
            "history",
            "archäologie",
            "archaeology",
            "kingdom",
            "ancient",
            "neolithikum",
            "seevölker",
        ],
        "nachrichten": ["news", "aktuell", "report", "journalism"],
        "sozial": ["social", "community", "network", "media"],
        "umwelt": ["environment", "climate", "nature", "ecology"],
        "raumfahrt": ["space", "rocket", "nasa", "astronomy"],
        "kultur": ["culture", "art", "kunst", "music", "musik", "tradition"],
        "wirtschaft": ["economy", "finance", "geld", "sparen", "market", "business"],
        "bildung": ["education", "learning", "school", "university"],
        "politik": ["politics", "government", "policy", "deutschland"],
        "reisen": ["travel", "trip", "destination", "tourism"],
        "essen": ["food", "kaffee", "coffee", "aroma", "recipe"],
        "sport": ["sports", "game", "fitness", "team"],
        "design": ["design", "architecture", "style"],
        "kriminalitat": ["crime", "law", "justice"],
        "militar": ["military", "war", "defense"],
        # Add more categories as needed
    }

    common_tags = set()
    for keyword in keywords:
        cleaned = clean_tag(keyword)
        if not cleaned:
            continue
        for common_tag, triggers in tag_mapping.items():
            if cleaned in triggers or cleaned == common_tag:
                common_tags.add(common_tag)
                break  # Stop after first match to avoid overlap

    # Limit to 5 tags max per article
    return list(common_tags)[:5]


def parse_pocket_csv():
    """Parse all CSV files in the pocket folder and generate common tags."""
    articles = []
    csv_files = glob.glob(os.path.join(POCKET_FOLDER, "*.csv"))
    if not csv_files:
        print(
            f"Warning: No .csv files found in {POCKET_FOLDER}. Please add your Pocket export CSV(s)."
        )
        return articles

    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"Warning: {csv_file} not found. Skipping.")
            continue
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Extract keywords from title and map to common tags
                keywords = extract_keywords_from_text(row["title"])
                tags = map_to_common_tags(keywords)
                articles.append(
                    {"url": row["url"], "title": row["title"], "tags": tags}
                )
        print(
            f"Loaded {len(articles)} articles from {os.path.basename(csv_file)} with common tags."
        )
    return articles


def tag_pocket_articles():
    """Tag Pocket articles from CSV and save to JSON."""
    print("Tagging Pocket articles from CSV files...")
    articles = parse_pocket_csv()
    if not articles:
        raise ValueError(f"No articles found in the CSV files in {POCKET_FOLDER}.")

    all_tags = set()
    for article in articles:
        all_tags.update(article["tags"])
    print(f"Generated {len(all_tags)} unique tags: {sorted(all_tags)}")

    # Save tagged articles
    with open(TAGGED_EXPORT_FILE, "w") as f:
        json.dump(articles, f)
    print(f"Saved {len(articles)} tagged articles to {TAGGED_EXPORT_FILE}.")

    # Save tag list for reference
    with open(TAG_MAPPING_FILE, "w") as f:
        json.dump(dict.fromkeys(all_tags), f)
    print(f"Saved tag list with {len(all_tags)} entries to {TAG_MAPPING_FILE}.")
    return articles


def import_tagged_articles():
    """Import tagged articles into Pocket."""
    print("Importing tagged articles into Pocket...")
    with open(TAGGED_EXPORT_FILE, "r") as f:
        articles = json.load(f)

    actions = []
    for article in articles:
        tags = ",".join(article["tags"]) if article["tags"] else ""
        actions.append(
            {
                "action": "add",
                "url": article["url"],
                "title": article["title"],
                "tags": tags,
            }
        )

    batch_size = 50
    for i in range(0, len(actions), batch_size):
        batch = actions[i : i + batch_size]
        try:
            pocket.bulk_add(actions=batch)
            print(f"Imported {len(batch)} articles.")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Error importing batch {i//batch_size + 1}: {str(e)}")


def main():
    """Main function to tag and import Pocket articles."""
    tagged_articles = tag_pocket_articles()
    import_tagged_articles()


if __name__ == "__main__":
    main()
