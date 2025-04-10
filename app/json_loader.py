from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

def load_json(file_path):
    with open(BASE_DIR / file_path, "r", encoding="utf-8") as f:
        return json.load(f)