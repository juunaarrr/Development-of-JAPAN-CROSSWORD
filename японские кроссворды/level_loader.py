import json
import os
from helpers import resource_path


def load_level(level_number):
    levels_dir = resource_path("levels")
    filename = os.path.join(levels_dir, f"level{level_number}.json")

    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return None

    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)