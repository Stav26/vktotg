import telebot
import logging
import vk
import os
import sys
import xml.etree.ElementTree as ET
from logger_config import setup_logger
from read_write_json import *



#Извлекаем из беседы в vk последнее сообщение и записываем last_message_id в файл
def vkapi():
    try:
        api = vk.API(access_token=token_vk, v = '5.199')
        full_list = api.messages.getConversations()
        last_message_id = int(full_list['items'][0]['conversation']['last_conversation_message_id'])
        if last_message_id != int(read_id):
            data["vk"]["last_message_id"] = last_message_id
            write_json_file(data)
            return full_list['items'][0]['last_message']['text']
        else:
            logging.info(f"Новые сообщения отсутсвуют\n")
            sys.exit(1)
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
    except:
        pass

if __name__ == "__main__":
    setup_logger()
    logging.info(f"Поиск и чтение json файла с настройками")
    
    if read_json_file() is not None:
       token_tg = read_json_file()["telegram"]["bot_token"]
       chat_id = read_json_file()["telegram"]["chat_id"]
       token_vk = read_json_file()["vk"]["access_token"]
       read_id = read_json_file()["vk"]["last_message_id"]
       logging.info(f"Запускаю скрипт {os.path.basename(__file__)}")
       logging.info(f"Извлечение из беседы в vk, id последнего сообщения и запись last_message_id в файл")
       vkapi()
       send()
    else:
        logging.error("Файл не найден, невозможно продолжить\n") 
        sys.exit(1)