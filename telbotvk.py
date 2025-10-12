import telebot
import logging
import vk
import os
import sys
from logger_config import setup_logger
from read_write_json import *

#Извлекаем из беседы в vk последнее сообщение и записываем last_message_id в файл
def get_last_message():
    try:
        api = vk.API(access_token=token_vk, v = '5.199')
        full_list = api.messages.getConversations()
        for items in full_list['items']:
            #Проверяем есть ли id чата указанного в settings в vk
            if items['last_message']['peer_id'] == chat_id_vk:
                last_message_id = items['last_message']['conversation_message_id']
                #Если чат найден проверяем есть ли id последнего сообщения в settings
                if last_message_id != read_id:
                    #Если id последнего сообщения не совпадаеют то записываем его в settings
                    data["vk"]["last_message_id"] = last_message_id
                    write_json_file(data)
                    #Возращаем текст последнего сообщения
                    return items['last_message']['text']
                else:
                    logging.info(f"Новые сообщения отсутсвуют\n")
                    sys.exit(1)
            else:
                logging.info(f"Чат в vk отсутсвует\n")
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
        telebot.TeleBot(token_tg).send_message(chat_id_tg, get_last_message())
        logging.info(f"Отправлено\n")
    except telebot.apihelper.ApiTelegramException as e:
        for attr in ['description']:
            if hasattr(e, attr):
                if not "Bad Request: message text is empty" in getattr(e, attr):
                    telebot.TeleBot(token_tg).send_message(chat_id_tg, e)
                    logging.error(f"{getattr(e, attr)}\n")
    except:
        pass

if __name__ == "__main__":
    setup_logger()
    logging.info(f"Поиск и чтение json файла с настройками")
    
    if read_json_file() is not None:
       token_tg = read_json_file()["telegram"]["bot_token"]
       chat_id_tg = read_json_file()["telegram"]["chat_id"]
       chat_id_vk = read_json_file()["vk"]["chat_id"]
       token_vk = read_json_file()["vk"]["access_token"]
       read_id = read_json_file()["vk"]["last_message_id"]
       logging.info(f"Запускаю скрипт {os.path.basename(__file__)}")
       logging.info(f"Извлечение из беседы в vk, id последнего сообщения и запись last_message_id в файл")
       get_last_message()
       send()
    else:
        logging.error("Файл не найден, невозможно продолжить\n") 
        sys.exit(1)


