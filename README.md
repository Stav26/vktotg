# vktotg
Sending messages from VK to telegrams
Для работы скрипта необходимо заполнить файл settings.xml, внести строчку в cron для переодического запуска скрипта. При работе скрипта создается папка log в который пишутся логи с разбивкой по дням.
В файле settings необходимо заполнить слдующие строки:
tg_token - токен выдаваемый при создании tg bot,
chat_id - id бота,
token - токен для подключения к api vk (https://vkhost.github.io выбрать Kate Mobile, следовать инструкциям)

Доп инфа:
Инфа по методу получения доступа к сообщениям - https://dev.vk.com/ru/method/messages.getConversations
