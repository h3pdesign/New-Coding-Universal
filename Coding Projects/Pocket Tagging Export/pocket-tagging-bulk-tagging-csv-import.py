import os
import time
import re
import json
import unicodedata
import csv
import glob
import spacy
import logging
import requests
from pocket import Pocket
from dotenv import load_dotenv

# Set up logging to file and console
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "pocket_import.log"))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# Load spaCy German model
nlp = spacy.load("de_core_news_sm")

# Load environment variables
load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    logging.error("Missing Pocket environment variables. Check your .env file.")
    raise ValueError("Missing Pocket credentials.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)

# Test Pocket API connection
logging.info("Testing Pocket API connection...")
try:
    response = pocket.get(count=1)
    if isinstance(response, tuple):
        data, headers = response
    else:
        data = response
    if data.get("status") == 1:
        logging.info(
            "API connection successful. Retrieved %d items.", len(data.get("list", {}))
        )
    else:
        logging.error("API returned unsuccessful status: %s", data)
        exit(1)
except Exception as e:
    logging.error("API connection failed: %s", str(e))
    exit(1)

# Define folder and file paths
POCKET_FOLDER = "/Users/h3p/Coding/New-Coding-Universal/Coding Projects/Pocket Tagging Export/pocket"
TAG_MAPPING_FILE = os.path.join(POCKET_FOLDER, "tag_mapping.json")
TAGGED_EXPORT_FILE = os.path.join(POCKET_FOLDER, "tagged_pocket_data.json")

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


def get_fallback_tag(title):
    """Extract a fallback tag from the title if no common tags are found."""
    doc = nlp(title)
    for token in doc:
        if (
            token.pos_ in ["NOUN", "PROPN"]
            and not token.is_stop
            and len(token.text) > 2
        ):
            cleaned = clean_tag(token.lemma_)
            if cleaned:
                return cleaned
    return "misc"  # Absolute fallback if no suitable noun/proper noun is found


def map_to_common_tags(keywords):
    """Map keywords to a curated set of common tags."""
    tag_mapping = {
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
    }
    common_tags = set()
    for keyword in keywords:
        cleaned = clean_tag(keyword)
        if not cleaned:
            continue
        for common_tag, triggers in tag_mapping.items():
            if cleaned in triggers or cleaned == common_tag:
                common_tags.add(common_tag)
                break
    return list(common_tags)[:5]


def parse_pocket_csv():
    """Parse all CSV files in the pocket folder and generate common tags."""
    articles = []
    csv_files = glob.glob(os.path.join(POCKET_FOLDER, "*.csv"))
    if not csv_files:
        logging.warning("No .csv files found in %s.", POCKET_FOLDER)
        return articles

    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            logging.warning("%s not found. Skipping.", csv_file)
            continue
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                expected_columns = {"title", "url"}
                if not expected_columns.issubset(reader.fieldnames):
                    logging.error(
                        "CSV %s missing required columns: %s",
                        csv_file,
                        expected_columns,
                    )
                    continue
                for row in reader:
                    keywords = extract_keywords_from_text(row["title"])
                    tags = map_to_common_tags(keywords)
                    if not tags:
                        tags = [get_fallback_tag(row["title"])]
                    articles.append(
                        {"url": row["url"], "title": row["title"], "tags": tags}
                    )
            logging.info(
                "Loaded %d articles from %s with common tags.",
                len(articles),
                os.path.basename(csv_file),
            )
        except Exception as e:
            logging.error("Error reading %s: %s", csv_file, str(e))
    return articles


def tag_pocket_articles():
    """Tag Pocket articles from CSV and save to JSON."""
    logging.info("Tagging Pocket articles from CSV files...")
    articles = parse_pocket_csv()
    if not articles:
        logging.error("No articles found in CSV files in %s. Aborting.", POCKET_FOLDER)
        return None

    all_tags = set()
    for article in articles:
        all_tags.update(article["tags"])
    logging.info("Generated %d unique tags: %s", len(all_tags), sorted(all_tags))

    try:
        with open(TAGGED_EXPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False)
        logging.info(
            "Saved %d tagged articles to %s.", len(articles), TAGGED_EXPORT_FILE
        )
    except Exception as e:
        logging.error("Error saving %s: %s", TAGGED_EXPORT_FILE, str(e))
        return None

    try:
        with open(TAG_MAPPING_FILE, "w", encoding="utf-8") as f:
            json.dump(dict.fromkeys(all_tags), f)
        logging.info(
            "Saved tag list with %d entries to %s.", len(all_tags), TAG_MAPPING_FILE
        )
    except Exception as e:
        logging.error("Error saving %s: %s", TAG_MAPPING_FILE, str(e))

    return articles


def import_tagged_articles():
    logging.info("Starting import of tagged articles into Pocket...")
    if not os.path.exists(TAGGED_EXPORT_FILE):
        logging.error("%s not found.", TAGGED_EXPORT_FILE)
        return

    with open(TAGGED_EXPORT_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    logging.info("Loaded %d articles from %s.", len(articles), TAGGED_EXPORT_FILE)

    actions = [
        {"action": "add", "url": a["url"], "title": a["title"], "tags": a["tags"]}
        for a in articles
    ]
    logging.info("Prepared %d actions.", len(actions))

    url = "https://getpocket.com/v3/send"
    headers = {"Content-Type": "application/json"}
    batch_size = 50
    total_batches = (len(actions) + batch_size - 1) // batch_size

    last_success = 0
    try:
        with open(LOG_FILE, "r") as log:
            for line in reversed(log.readlines()):
                if "Batch" in line and "successfully imported" in line:
                    last_success = int(line.split("Batch")[1].split()[0])
                    break
        logging.info("Last successful batch: %d", last_success)
    except:
        logging.info("No prior log found, starting fresh.")

    start_index = last_success * batch_size
    for i in range(start_index, len(actions), batch_size):
        batch_num = i // batch_size + 1
        batch = actions[i : i + batch_size]
        logging.info(
            "Processing batch %d of %d with %d articles...",
            batch_num,
            total_batches,
            len(batch),
        )
        payload = {
            "consumer_key": POCKET_CONSUMER_KEY,
            "access_token": POCKET_ACCESS_TOKEN,
            "actions": batch,
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            data = response.json()
            if response.status_code == 200 and data.get("status") == 1:
                logging.info(
                    "Batch %d successfully imported %d articles.", batch_num, len(batch)
                )
            else:
                logging.error(
                    "Batch %d failed: HTTP %d, response: %s",
                    batch_num,
                    response.status_code,
                    data,
                )
                break
            time.sleep(1)
        except Exception as e:
            logging.error("Batch %d error: %s", batch_num, str(e))
            break

    logging.info("Import completed. Processed up to batch %d.", batch_num)


def main():
    """Main function to tag and import Pocket articles."""
    if os.path.exists(TAGGED_EXPORT_FILE):
        logging.info(
            "Found existing %s. Skipping tagging and proceeding to import.",
            TAGGED_EXPORT_FILE,
        )
        import_tagged_articles()
    else:
        tagged_articles = tag_pocket_articles()
        if tagged_articles:
            import_tagged_articles()
        else:
            logging.error("No articles tagged, skipping import.")


if __name__ == "__main__":
    main()
