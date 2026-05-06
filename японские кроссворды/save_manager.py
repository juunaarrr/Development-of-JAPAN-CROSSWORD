import json
import os

SAVE_FILE = "save.json"


class SaveManager:
    @staticmethod
    def save(level_num, cells, lives):
        """сохраняет прогресс в файл"""
        data = {
            "level_num": level_num,
            "cells": cells,
            "lives": lives
        }
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load():
        """загружает прогресс из файла"""
        if not os.path.exists(SAVE_FILE):
            return None

        # проверка на пустой файл
        if os.path.getsize(SAVE_FILE) == 0:
            os.remove(SAVE_FILE)
            return None

        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # если файл повреждён, удаляем его
            os.remove(SAVE_FILE)
            return None

    @staticmethod
    def delete():
        """удаляет файл сохранения"""
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)