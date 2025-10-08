import logging
import os
from datetime import datetime

def setup_logger():
    # Создаем папку для логов, если она не существует
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Формируем имя файла с текущей датой
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"log_{current_date}.log"
    log_filepath = os.path.join(log_dir, log_filename)
    
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    if __name__ == "__main__":
        setup_logger()  