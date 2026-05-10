import json
import os

PROGRESS_FILE = "progress.json"


class ProgressManager:
    @staticmethod
    #загружает список пройденных уровней
    def load():
        if not os.path.exists(PROGRESS_FILE):
            return []
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("completed_levels", [])
        except:
            return []

    @staticmethod
    #сохраняет список пройденных уровней
    def save(completed_levels):
        data = {"completed_levels": completed_levels}
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    #отмечает уровень как пройденный
    def add_level(level_num):
        completed = ProgressManager.load()
        if level_num not in completed:
            completed.append(level_num)
            ProgressManager.save(completed)

    @staticmethod
    #проверяет пройден ли уровень
    def is_completed(level_num):
        return level_num in ProgressManager.load()

    @staticmethod
    #удаляет файл (сбрасывает прогресс)
    def reset():
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)