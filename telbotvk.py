import telebot
import logging
import vk
import os
import sys
import xml.etree.ElementTree as ET
from logger_config import setup_logger

filename = 'settings.xml'
setup_logger()

logging.info(f"Запускаю скрипт {os.path.basename(__file__)}")
logging.info(f"Поиск xml файла с настройками")
def path_to_xml():
    # Получаем путь к текущей директории, где находится скрипт
    search_path = os.path.dirname(os.path.abspath(__file__))
    
    # Используем os.walk для обхода всех директорий и подкаталогов
    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return os.path.join(dirpath, filename)  # Возвращаем полный путь к файлу
    
    return None  # Если файл не найден, возвращаем None

#Получаем корневой элемент xml файла
def root_xml():
    tree = ET.parse(path_to_xml())
    root = tree.getroot()
    return tree, root

tree, root = root_xml()

logging.info(f"Чтение xml файла с настройками")
#Читаем xml файл в котором токены vk/tg, id сообщения в вк, chat_id в тг
def read_xml():
    for r in root:
        # Проверяем тег каждого элемента и извлекаем текст
        if r.tag == 'tg_token':
            token_tg = r.text
        elif r.tag == 'chat_id':
            chat_id = r.text
        elif r.tag == 'last_id':
            read_id = r.text
        elif r.tag == 'token':
            token_vk = r.text

    return token_tg, chat_id, read_id, token_vk

token_tg, chat_id, read_id, token_vk = read_xml()  

logging.info(f"Извлечение из беседы в vk последнего сообщения и запись last_message_id в файл")
#Извлекаем из беседы в vk последнее сообщение и записываем last_message_id в файл
def vkapi():
    try:
        api = vk.API(access_token=token_vk, v = '5.199')
        full_list = api.messages.getConversations()
        last_message_id = int(full_list['items'][0]['conversation']['last_conversation_message_id'])
        if last_message_id != int(read_id):
            for r in root:
                if r.tag == 'last_id':
                    r.text = str(last_message_id)
                    tree.write(path_to_xml())
            return full_list['items'][0]['last_message']['text']
    except vk.exceptions.VkAPIError as e:
        logging.error(f"{e}")
        return e
    except Exception as e:
        logging.error(f"{e}")
        return e  

          
#Отправляем содержание сообщения в бот                 
def send():
    try:
        logging.info(f"Отправляю содержание сообщения в бот")          
        telebot.TeleBot(token_tg).send_message(chat_id, vkapi())
        logging.info(f"Отправлено\n")
    except telebot.apihelper.ApiTelegramException as e:
        for attr in ['description']:
            if hasattr(e, attr):
                if not "Bad Request: message text is empty" in getattr(e, attr):
                    telebot.TeleBot(token_tg).send_message(chat_id, e)
                    logging.error(f"{getattr(e, attr)}\n")
                else:
                    logging.info(f"Новые сообщения отсутсвуют\n")
    except:
        pass
send()