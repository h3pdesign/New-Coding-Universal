import os
import time
import re
import json
import unicodedata
import csv
import spacy
from pocket import Pocket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing Pocket environment variables. Check your .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)

# Load SpaCy German model
nlp = spacy.load("de_core_news_sm")

TAG_MAPPING_FILE = "tag_mapping.json"
CLEANED_EXPORT_FILE = "cleaned_pocket_data.json"


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
    doc = nlp(cleaned)
    return len(doc) == 1 and doc[0].pos_ in {"NOUN", "PROPN"}


def is_plural(tag):
    doc = nlp(tag)
    return (
        len(doc) == 1 and doc[0].tag_ == "NN" and doc[0].morph.get("Number") == ["Plur"]
    )


def get_singular_form(tag):
    doc = nlp(tag)
    if is_plural(tag):
        lemma = doc[0].lemma_
        return lemma if nlp(lemma)[0].pos_ in {"NOUN", "PROPN"} else tag
    return tag


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
            if is_plural(cleaned):
                singular = get_singular_form(cleaned)
                if singular != cleaned and singular in tags:
                    consolidated[tag] = singular
                    print(f"Consolidated plural '{tag}' → '{singular}'")
                else:
                    consolidated[tag] = cleaned
            else:
                consolidated[tag] = cleaned
    return consolidated


def parse_pocket_csv(csv_file):
    articles = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags = row["tags"].split("|") if row["tags"] else []
