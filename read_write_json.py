import os
import json
import sys
import logging
from logger_config import setup_logger

filename = 'settings.json'
setup_logger()

def path_to_json():
    # Получаем путь к текущей директории, где находится скрипт
    search_path = os.path.dirname(os.path.abspath(__file__))
    # Используем os.walk для обхода всех директорий и подкаталогов
    try:
        for dirpath, dirnames, filenames in os.walk(search_path):
            if filename in filenames:
                return os.path.join(dirpath, filename)  # Возвращаем полный путь к файлу
    except FileNotFoundError:
        return None
    
#Читаем файл
def read_json_file():
    if path_to_json() is None:
        return None
    try:
        with open(path_to_json(), 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        logging.error("Ошибка: Не удалось декодировать JSON из файла.") 
        return None

data = read_json_file()

#Записываем файл
def write_json_file(data):
    with open(path_to_json(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    read_json_file()
    write_json_file(data) 

