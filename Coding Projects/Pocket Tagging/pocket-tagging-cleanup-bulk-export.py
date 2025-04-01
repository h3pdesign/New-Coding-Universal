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

# Load spaCy German model (since some content is in German)
nlp = spacy.load("de_core_news_sm")

# Load environment variables
load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing Pocket environment variables. Check your .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)

# Define folder and file paths
POCKET_FOLDER = (
    "/Users/h3p/Coding/New-Coding-Universal/Coding Projects/Pocket Tagging/pocket"
)
TAG_MAPPING_FILE = os.path.join(POCKET_FOLDER, "tag_mapping.json")
CLEANED_EXPORT_FILE = os.path.join(POCKET_FOLDER, "cleaned_pocket_data.json")

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


def is_single_noun(tag):
    """Check if a tag is a single noun using spaCy."""
    cleaned = clean_tag(tag)
    if not cleaned:
        return False
    doc = nlp(cleaned)
    return len(doc) == 1 and doc[0].pos_ == "NOUN"


def extract_tags_from_text(text):
    """Extract potential tags from text using spaCy."""
    doc = nlp(text)
    tags = set()
    for token in doc:
        # Focus on nouns, proper nouns, and compounds
        if (
            token.pos_ in ["NOUN", "PROPN"]
            and not token.is_stop
            and len(token.text) > 2
        ):
            cleaned = clean_tag(token.lemma_)
            if cleaned and is_single_noun(cleaned):
                tags.add(cleaned)
    return tags


def consolidate_tags(tags):
    """Consolidate tags using a mapping and spaCy lemmatization."""
    tag_mapping = {
        "abschiebeflieger": "abschiebeflug",
        "abschiebeflüge": "abschiebeflug",
        "abmahnagentur": "abmahnung",
        "abkassieren": "abmahnung",
        "§stgb": "stgb",
        "°sound": "sound",
        "€millionorder": "millionorder",
        ":scale": "scale",
        "geschichte": "geschichte",
        "wiki": "wikipedia",
        "archäologie": "archaeologie",
        "finanzkrise": "finanzkrise",
        "bibel|christentum": "bibel",
        "you tube": "youtube",
        "deutschland": "deutschland",
        "politik": "politik",
        "freimaurer": "freimaurerei",
        "love": "liebe",
        "zensur": "zensur",
        "seevölker": "seevoelker",
        "neolithikum": "neolithikum",
        "tech": "technologie",
        "coding": "code",
        "blog": "blog",
        "news": "nachrichten",
        "social": "sozial",
        "aroma": "aroma",
        "geldsparen": "sparen",
        "kaffee": "kaffee",
        "trick": "trick",
    }
    consolidated = {}
    for tag in tags:
        cleaned = clean_tag(tag)
        if not cleaned or not is_single_noun(cleaned):
            print(f"Skipping invalid tag '{tag}' → '{cleaned}'")
            continue
        doc = nlp(cleaned)
        lemma = doc[0].lemma_ if doc else cleaned

        if tag in tag_mapping:
            consolidated[tag] = tag_mapping[tag]
        elif cleaned in tag_mapping:
            consolidated[tag] = tag_mapping[cleaned]
        elif lemma in tag_mapping:
            consolidated[tag] = tag_mapping[lemma]
        else:
            consolidated[tag] = lemma if is_single_noun(lemma) else cleaned
    return consolidated


def parse_pocket_csv():
    """Parse all CSV files in the pocket folder and assign tags."""
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
                existing_tags = row["tags"].split("|") if row["tags"] else []
                # Extract tags from title if no or few existing tags
                if len(existing_tags) < 2:  # Adjust threshold as needed
                    new_tags = extract_tags_from_text(row["title"])
                    existing_tags.extend(new_tags)
                articles.append(
                    {"url": row["url"], "title": row["title"], "tags": existing_tags}
                )
        print(
            f"Loaded {len(articles)} articles from {os.path.basename(csv_file)} so far."
        )
    return articles


def clean_pocket_tags_offline():
    """Clean Pocket tags offline from CSV files and apply tagging."""
    print("Cleaning Pocket tags offline from CSV files and applying tags...")
    articles = parse_pocket_csv()
    if not articles:
        raise ValueError(f"No articles found in the CSV files in {POCKET_FOLDER}.")

    all_tags = set()
    for article in articles:
        all_tags.update(article["tags"])
    print(f"Found {len(all_tags)} unique tags: {sorted(all_tags)}")

    tag_mapping = consolidate_tags(all_tags)
    print("Tag consolidation mapping:", tag_mapping)

    cleaned_articles = []
    for article in articles:
        old_tags = set(article["tags"])
        new_tags = set()
        for tag in old_tags:
            canonical_tag = tag_mapping.get(tag, clean_tag(tag))
            if canonical_tag:
                new_tags.add(canonical_tag)
        cleaned_articles.append(
            {"url": article["url"], "title": article["title"], "tags": list(new_tags)}
        )

    with open(CLEANED_EXPORT_FILE, "w") as f:
        json.dump(cleaned_articles, f)
    print(f"Saved {len(cleaned_articles)} cleaned articles to {CLEANED_EXPORT_FILE}.")

    with open(TAG_MAPPING_FILE, "w") as f:
        json.dump(tag_mapping, f)
    print(f"Saved tag mapping with {len(tag_mapping)} entries to {TAG_MAPPING_FILE}.")
    return cleaned_articles


def archive_all_articles():
    """Archive all existing articles in Pocket."""
    print("Archiving all existing articles...")
    try:
        response = pocket.get(state="all", detailType="simple")
        articles = response[0].get("list", {})
    except Exception as e:
        print(f"Error fetching articles: {str(e)}")
        return

    actions = [{"action": "archive", "item_id": item_id} for item_id in articles.keys()]
    batch_size = 50
    for i in range(0, len(actions), batch_size):
        batch = actions[i : i + batch_size]
        try:
            pocket.bulk_add(actions=batch)
            print(f"Archived {len(batch)} articles.")
            time.sleep(1)
        except Exception as e:
            print(f"Error archiving batch {i//batch_size + 1}: {str(e)}")


def reimport_cleaned_articles():
    """Reimport cleaned articles into Pocket."""
    print("Reimporting cleaned articles...")
    with open(CLEANED_EXPORT_FILE, "r") as f:
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
            time.sleep(1)
        except Exception as e:
            print(f"Error importing batch {i//batch_size + 1}: {str(e)}")


def cleanup_pocket_tags():
    """Main function to clean up Pocket tags."""
    cleaned_articles = clean_pocket_tags_offline()
    archive_all_articles()
    reimport_cleaned_articles()


if __name__ == "__main__":
    cleanup_pocket_tags()
