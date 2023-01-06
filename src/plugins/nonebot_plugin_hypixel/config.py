from pathlib import Path
import json
import os

Config_path = Path() / "data" / "hypixel" / "config.json"

New_map = {
    "api_key": "API_KEY"
}

def get_config():
    if os.path.exists(Config_path):
        with open(Config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        if os.path.exists(Path() / "data" / "hypixel") == False:
            os.makedirs(Path() / "data" / "hypixel")
        with open(Config_path, 'w', encoding='utf-8') as f:
            json.dump(New_map, f, ensure_ascii=False, indent=4)
        with open(Config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

api_key = get_config()['api_key']
