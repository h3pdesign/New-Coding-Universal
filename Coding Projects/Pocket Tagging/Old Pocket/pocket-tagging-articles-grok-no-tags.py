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

# Load environment variables
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


def is_valid_tag(tag):
    """Check if a tag is a valid noun or proper noun using spaCy."""
    cleaned = clean_tag(tag)
    if not cleaned:
        return False
    doc = nlp(cleaned)
    return len(doc) == 1 and doc[0].pos_ in ["NOUN", "PROPN"]


def extract_tags_from_text(text):
    """Extract potential tags from text using spaCy."""
    doc = nlp(text)
    tags = set()
    for token in doc:
        # Focus on nouns and proper nouns, exclude stop words and short tokens
        if (
            token.pos_ in ["NOUN", "PROPN"]
            and not token.is_stop
            and len(token.text) > 2
            and is_valid_tag(token.lemma_)
        ):
            tags.add(token.lemma_)
    return tags


def consolidate_tags(tags):
    """Consolidate tags using a predefined mapping."""
    tag_mapping = {
        # General cleanup
        "abschiebeflieger": "abschiebeflug",
        "abschiebeflüge": "abschiebeflug",
        "abmahnagentur": "abmahnung",
        "abkassieren": "abmahnung",
        "§stgb": "stgb",
        "°sound": "sound",
        "€millionorder": "millionorder",
        ":scale": "scale",
        "wiki": "wikipedia",
        "you tube": "youtube",
        # Domain-specific from your CSV
        "tech": "technologie",
        "coding": "code",
        "blog": "blog",
        "news": "nachrichten",
        "social": "sozial",
        "aroma": "aroma",
        "geldsparen": "sparen",
        "kaffee": "kaffee",
        "trick": "trick",
        "archäologie": "archaeologie",
        "geschichte": "geschichte",
        "politik": "politik",
        "finanzkrise": "finanzkrise",
        "freimaurer": "freimaurerei",
        "love": "liebe",
        "zensur": "zensur",
        "seevölker": "seevoelker",
        "neolithikum": "neolithikum",
        # Additional inferred categories
        "science": "wissenschaft",
        "ai": "ki",
        "health": "gesundheit",
        "history": "geschichte",
        "archaeology": "archaeologie",
        "technology": "technologie",
        "gaming": "spiele",
        "energy": "energie",
        "environment": "umwelt",
        "medicine": "medizin",
        "space": "raumfahrt",
        "culture": "kultur",
        "economy": "wirtschaft",
        "education": "bildung",
        "military": "militar",
        "crime": "kriminalitat",
        "travel": "reisen",
        "food": "essen",
        "art": "kunst",
        "design": "design",
        "music": "musik",
        "sports": "sport",
    }
    consolidated_tags = set()
    for tag in tags:
        cleaned = clean_tag(tag)
        if not cleaned or not is_valid_tag(cleaned):
            print(f"Skipping invalid tag '{tag}' → '{cleaned}'")
            continue
        # Apply mapping if available, otherwise use lemmatized form
        canonical_tag = tag_mapping.get(cleaned, cleaned)
        if canonical_tag:
            consolidated_tags.add(canonical_tag)
    return consolidated_tags


def parse_pocket_csv():
    """Parse all CSV files in the pocket folder and generate tags."""
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
                # Generate tags from title since all tags are removed
                generated_tags = extract_tags_from_text(row["title"])
                consolidated_tags = consolidate_tags(generated_tags)
                articles.append(
                    {
                        "url": row["url"],
                        "title": row["title"],
                        "tags": list(consolidated_tags),
                    }
                )
        print(
            f"Loaded {len(articles)} articles from {os.path.basename(csv_file)} with generated tags."
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

    # Save tag mapping for reference
    with open(TAG_MAPPING_FILE, "w") as f:
        json.dump(dict.fromkeys(all_tags), f)  # Simple list of tags used
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
