import json
import os


def load_level(level_number):
    filename = f"levels/level{level_number}.json"  # ← используем level_number

    if not os.path.exists(filename):
        print(f"Файл {filename} не найден")
        return None

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
