import os
import time
import re
import json
import unicodedata
from pocket import Pocket
from dotenv import load_dotenv
import spacy

load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing Pocket environment variables. Check your .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)
nlp = spacy.load("de_core_news_sm")

TAG_MAPPING_FILE = "tag_mapping.json"


def clean_tag(tag):
    normalized = "".join(
        c for c in unicodedata.normalize("NFKD", tag) if unicodedata.category(c) != "Mn"
    )
    unwanted = r"[°€?!@#$%^&*()+={}[\]|\\:;\"'<>,./\s]+"
    cleaned = re.sub(unwanted, "-", normalized).lower().strip("-")
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned if cleaned and len(cleaned) <= 50 else ""


def is_single_noun(tag):
    cleaned = clean_tag(tag)
    return not cleaned.endswith(("ly", "ed", "ing", "al", "ive"))


def is_plural(tag):
    cleaned = clean_tag(tag)
    doc = nlp(cleaned)
    return any(token.morph.get("Number") == "Plur" for token in doc)


def get_singular_form(tag):
    cleaned = clean_tag(tag)
    doc = nlp(cleaned)
    for token in doc:
        if token.morph.get("Number") == "Plur":
            if cleaned.endswith("en"):
                return cleaned[:-2]
            if cleaned.endswith("e"):
                return cleaned[:-1]
    return cleaned


def consolidate_tags(tags):
    tag_mapping = {
        "abschiebeflieger": "abschiebeflug",
        "abschiebeflüge": "abschiebeflug",
        "abmahnagentur": "abmahnung",
        "abkassieren": "abmahnung",
        "§stgb": "stgb",
        "°sound": "sound",
        "€millionorder": "millionorder",
        ":scale": "scale",
    }
    consolidated = {}
    for tag in tags:
        cleaned = clean_tag(tag)
        if not cleaned or not is_single_noun(cleaned):
            print(f"Skipping invalid tag '{tag}' → '{cleaned}'")
            continue
        if tag in tag_mapping:
            consolidated[tag] = tag_mapping[tag]
        elif cleaned in tag_mapping:
            consolidated[tag] = tag_mapping[cleaned]
        else:
            if is_plural(tag):
                singular = get_singular_form(tag)
                if singular in tag_mapping.values() or singular in tags:
                    consolidated[tag] = singular
                    print(f"Consolidated plural '{tag}' → '{singular}'")
                else:
                    consolidated[tag] = cleaned
            else:
                consolidated[tag] = cleaned
    return consolidated


def cleanup_pocket_tags_by_tag():
    print("Starting Pocket tag cleanup by tag...")
    # List of tags to consolidate (prioritize problematic ones)
    tags_to_clean = [
        "abschiebeflieger",
        "abschiebeflug",
        "abschiebeflüge",
        "abmahnagentur",
        "abkassieren",
        "§stgb",
        "°sound",
        "€millionorder",
        ":scale",
    ]
    all_tags = set(tags_to_clean)
    tag_mapping = consolidate_tags(all_tags)
    print("Tag consolidation mapping:", tag_mapping)

    for old_tag in tags_to_clean:
        try:
            response = pocket.get(tag=old_tag, detailType="complete")
            articles = response[0].get("list", {})
            print(f"Found {len(articles)} articles with tag '{old_tag}'")
        except Exception as e:
            print(f"Error fetching articles for tag '{old_tag}': {str(e)}")
            continue

        actions = []
        for item_id, article in articles.items():
            old_tags = set(article.get("tags", {}).keys())
            new_tags = set()
            for tag in old_tags:
                canonical_tag = tag_mapping.get(tag, clean_tag(tag))
                if canonical_tag:
                    new_tags.add(canonical_tag)
            if old_tags != new_tags:
                actions.append(
                    {
                        "action": "tags_replace",
                        "item_id": item_id,
                        "tags": ",".join(new_tags),
                    }
                )

        batch_size = 50
        for i in range(0, len(actions), batch_size):
            batch = actions[i : i + batch_size]
            try:
                pocket.bulk_add(actions=batch)
                print(f"Updated {len(batch)} articles for tag '{old_tag}'.")
                time.sleep(1)
            except Exception as e:
                print(
                    f"Error updating batch {i//batch_size + 1} for '{old_tag}': {str(e)}"
                )

    with open(TAG_MAPPING_FILE, "w") as f:
        json.dump(tag_mapping, f)
    print(f"Saved tag mapping with {len(tag_mapping)} entries to {TAG_MAPPING_FILE}.")
    print("Pocket tag cleanup by tag completed.")


if __name__ == "__main__":
    cleanup_pocket_tags_by_tag()
