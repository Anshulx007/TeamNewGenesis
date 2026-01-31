import json
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


DOCUMENTS = load_json("documents.json")
SCHEMES = load_json("schemes.json")


def get_document_info(message: str):
    text = message.lower()
    for key, value in DOCUMENTS.items():
        if key in text:
            return key, value
    return None, None


def get_scheme_info(message: str):
    text = message.lower()
    for key, value in SCHEMES.items():
        if key in text:
            return key, value
    return None, None
