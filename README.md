# echo-server

Простой сервер, который принимает сообщения от клиента в локальной сети и выводит их в консоль.

Самая новая и стабильная версия [здесь](https://github.com/nikkonst2009/echo-server/tree/security/ip-filtering-and-saving-messages)

## Как работает
#### 1. Выводит порт сервера.
#### 2. Выводит все сообщения, переданные по локальной сети, в консоль (в кодировке UTF-8).

## Как использовать
#### 1. Соберите [echo-server](https://github.com/nikkonst2009/echo-server) с помощью
Linux: ```pyinstaller ./main.py --onefile```

Windows: ```pyinstaller main.py --onefile```
#### 1.1. Или скачайте [готовое приложение](https://github.com/nikkonst2009/echo-server/releases).

#### 2. Запустите приложение.
#### 3. Подключитесь с клиента.
##### IP-адрес можно найти с помощью команды:
   Linux: ```hostname -I```
   
   Windows: ```ipconfig``` и ищите ipv4

## Требования:
#### 1. Сервер и клиент должны быть подключены к одной сети Wi-Fi.
